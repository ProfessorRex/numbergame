package com.numgame.python.console;

import android.animation.ArgbEvaluator;
import android.animation.AnimatorSet;
import android.animation.ObjectAnimator;
import android.animation.ValueAnimator;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.GradientDrawable;
import android.content.SharedPreferences;
import android.content.res.ColorStateList;
import android.content.DialogInterface;
import android.media.AudioManager;
import android.media.ToneGenerator;
import android.os.Build;
import android.util.Base64;
import android.view.inputmethod.EditorInfo;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.Switch;
import android.widget.TextView;
import android.view.Window;
import android.view.Gravity;
import android.view.animation.DecelerateInterpolator;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    private static final String SETTINGS_FILE = "number_game_settings";
    private static final String DARK_MODE_KEY = "dark_mode";
    private static final String SAVED_GAME_KEY = "saved_game";
    private static final String HIGH_SCORE_POPUP_KEY = "high_score_popup_shown";
    private static final String HIGH_SCORE_FILE = "numbergame-highscore.txt";

    private NumberGameEngine game;
    private LinearLayout gameRoot;
    private LinearLayout clueContainer;
    private ScrollView clueScrollView;
    private TextView titleView;
    private TextView statsView;
    private TextView livesView;
    private TextView pointsOverlayView;
    private TextView rangeView;
    private TextView solutionCountView;
    private TextView messageView;
    private EditText answerInput;
    private Button actionButton;
    private ImageButton settingsButton;
    private boolean darkMode;
    private boolean gameStarted;
    private boolean gameOver;
    private boolean highScorePopupShown;
    private ToneGenerator soundGenerator;
    private int currentMinimum;
    private int currentMaximum;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        darkMode = getSharedPreferences(SETTINGS_FILE, MODE_PRIVATE)
            .getBoolean(DARK_MODE_KEY, true);
        setContentView(R.layout.activity_game);
        soundGenerator = new ToneGenerator(AudioManager.STREAM_MUSIC, 65);
        game = new NumberGameEngine();
        gameRoot = findViewById(R.id.gameRoot);
        clueContainer = findViewById(R.id.clueContainer);
        clueScrollView = findViewById(R.id.clueScrollView);
        titleView = findViewById(R.id.tvTitle);
        statsView = findViewById(R.id.tvStats);
        livesView = findViewById(R.id.tvLives);
        pointsOverlayView = findViewById(R.id.tvPointsEarned);
        rangeView = findViewById(R.id.tvRange);
        solutionCountView = findViewById(R.id.tvSolutionCount);
        messageView = findViewById(R.id.tvMessage);
        answerInput = findViewById(R.id.etAnswer);
        actionButton = findViewById(R.id.btnAction);
        settingsButton = findViewById(R.id.btnSettings);
        actionButton.setOnClickListener(view -> handleAction());
        settingsButton.setOnClickListener(view -> showSettings());
        int[] digitButtonIds = {R.id.btnDigit0, R.id.btnDigit1, R.id.btnDigit2,
                R.id.btnDigit3, R.id.btnDigit4, R.id.btnDigit5, R.id.btnDigit6,
                R.id.btnDigit7, R.id.btnDigit8, R.id.btnDigit9};
        for (int digit = 0; digit < digitButtonIds.length; digit++) {
            final int value = digit;
            findViewById(digitButtonIds[digit]).setOnClickListener(view -> appendDigit(value));
        }
        findViewById(R.id.btnClear).setOnClickListener(view -> answerInput.setText(""));
        findViewById(R.id.btnBackspace).setOnClickListener(view -> deleteLastDigit());
        answerInput.setOnEditorActionListener((view, actionId, event) -> {
            if (actionId == EditorInfo.IME_ACTION_DONE) {
                handleAction();
                return true;
            }
            return false;
        });
        applyPalette();
        updateStats();
        offerContinueIfSavedGame();
    }

    private void showSettings() {
        LinearLayout panel = new LinearLayout(this);
        panel.setOrientation(LinearLayout.VERTICAL);
        panel.setPadding(dp(8), dp(4), dp(8), dp(4));

        TextView questionLabel = settingsLabel("Question: " + (game.getQuestionsAnswered() + 1));
        panel.addView(questionLabel);

        String enteredSeed = answerInput.getText().toString().trim();
        boolean showSeed = gameStarted || gameOver
            ? !game.usesRandomSeed() : !enteredSeed.isEmpty();
        TextView seedLabel = settingsLabel(gameStarted || gameOver
            ? "Seed: " + game.getCurrentSeed() : "Seed: " + enteredSeed);
        seedLabel.setVisibility(showSeed ? View.VISIBLE : View.GONE);
        panel.addView(seedLabel);

        TextView highScoreLabel = settingsLabel("Random-play high score: " + readHighScore());
        panel.addView(highScoreLabel);

        Button saveButton = new Button(this);
        saveButton.setText("Save game");
        saveButton.setEnabled(gameStarted);
        saveButton.setTextColor(Color.WHITE);
        saveButton.setBackground(buttonBackground(
            darkMode ? Color.rgb(83, 185, 168) : Color.rgb(25, 121, 111),
            darkMode ? Color.rgb(111, 205, 188) : Color.rgb(18, 96, 87)));
        saveButton.setOnClickListener(view -> {
            saveProgress();
            saveButton.setText("Saved");
        });
        panel.addView(saveButton);

        LinearLayout row = new LinearLayout(this);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(dp(8), dp(8), dp(8), dp(8));
        TextView label = settingsLabel("Dark mode");
        label.setTextSize(16);
        row.addView(label, new LinearLayout.LayoutParams(0,
            LinearLayout.LayoutParams.WRAP_CONTENT, 1));
        Switch toggle = new Switch(this);
        toggle.setChecked(darkMode);
        row.addView(toggle, new LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.WRAP_CONTENT,
            LinearLayout.LayoutParams.WRAP_CONTENT));
        panel.addView(row);

        AlertDialog[] dialogRef = new AlertDialog[1];
        toggle.setOnCheckedChangeListener((button, enabled) -> {
            darkMode = enabled;
            getSharedPreferences(SETTINGS_FILE, MODE_PRIVATE).edit()
                .putBoolean(DARK_MODE_KEY, enabled).apply();
            applyPalette();
            int text = darkMode ? Color.rgb(230, 242, 238) : Color.rgb(32, 49, 46);
            questionLabel.setTextColor(text);
            seedLabel.setTextColor(text);
            highScoreLabel.setTextColor(text);
            label.setTextColor(text);
                saveButton.setBackground(buttonBackground(
                    darkMode ? Color.rgb(83, 185, 168) : Color.rgb(25, 121, 111),
                    darkMode ? Color.rgb(111, 205, 188) : Color.rgb(18, 96, 87)));
            if (dialogRef[0] != null) {
            styleDialog(dialogRef[0]);
            }
        });

        dialogRef[0] = showThemedDialog(new AlertDialog.Builder(this)
            .setTitle("Settings")
            .setView(panel)
            .setNeutralButton("Restart game", (dialog, which) -> restartGame())
            .setPositiveButton(android.R.string.ok, null));
    }

    private void handleAction() {
        if (!gameStarted || gameOver) {
            startGame();
            return;
        }
        submitAnswer();
    }


        private TextView settingsLabel(String text) {
        TextView label = new TextView(this);
        label.setText(text);
        label.setTextSize(14);
        label.setTextColor(darkMode ? Color.rgb(230, 242, 238) : Color.rgb(32, 49, 46));
        label.setPadding(dp(8), dp(8), dp(8), dp(8));
        return label;
        }

        private AlertDialog showThemedDialog(AlertDialog.Builder builder) {
        AlertDialog dialog = builder.create();
        dialog.show();
        styleDialog(dialog);
        return dialog;
        }

        private void styleDialog(AlertDialog dialog) {
        int surface = darkMode ? Color.rgb(29, 47, 43) : Color.rgb(255, 255, 255);
        int text = darkMode ? Color.rgb(230, 242, 238) : Color.rgb(32, 49, 46);
        int accent = darkMode ? Color.rgb(111, 205, 188) : Color.rgb(25, 121, 111);
        Window window = dialog.getWindow();
        if (window != null) {
            window.setBackgroundDrawable(new ColorDrawable(surface));
        }
        TextView title = dialog.findViewById(androidx.appcompat.R.id.alertTitle);
        TextView message = dialog.findViewById(android.R.id.message);
        if (title != null) title.setTextColor(text);
        if (message != null) message.setTextColor(text);
        int[] buttonIds = {DialogInterface.BUTTON_POSITIVE, DialogInterface.BUTTON_NEGATIVE,
            DialogInterface.BUTTON_NEUTRAL};
        for (int buttonId : buttonIds) {
            Button button = dialog.getButton(buttonId);
            if (button != null) button.setTextColor(accent);
        }
        }
    private void startGame() {
        Long seed = null;
        String seedText = answerInput.getText().toString().trim();
        if (!seedText.isEmpty()) {
            try {
                seed = Long.parseLong(seedText);
            } catch (NumberFormatException exception) {
                messageView.setText("Seed must be a whole number.");
                return;
            }
        }
        gameStarted = true;
        gameOver = false;
        highScorePopupShown = false;
        getSharedPreferences(SETTINGS_FILE, MODE_PRIVATE).edit()
            .remove(HIGH_SCORE_POPUP_KEY).apply();
        clueContainer.removeAllViews();
        rangeView.setText("");
        solutionCountView.setText("");
        answerInput.setText("");
        answerInput.setEnabled(false);
        actionButton.setText("Preparing question...");
        actionButton.setEnabled(false);
        messageView.setVisibility(View.VISIBLE);
        messageView.setText("Find a number that matches every rule.");
        updateStats();
        game.startGame(1, seed, this::showQuestion);
        saveProgress();
    }

    private void showQuestion(NumberGameEngine.Question question) {
        runOnUiThread(() -> {
            if (isFinishing() || isDestroyed()) {
                return;
            }
            clueContainer.removeAllViews();
            currentMinimum = question.minimum;
            currentMaximum = question.maximum;
            for (NumberGameEngine.Clue clue : question.clues) {
                TextView clueView = new TextView(this);
                clueView.setText(clue.text);
                clueView.setTextColor(darkMode ? Color.rgb(230, 242, 238) : Color.rgb(32, 49, 46));
                clueView.setTextSize(14);
                clueView.setPadding(dp(8), dp(5), dp(8), dp(5));
                GradientDrawable background = new GradientDrawable();
                background.setColor(darkMode ? Color.rgb(38, 58, 53) : Color.rgb(232, 242, 239));
                background.setCornerRadius(dp(5));
                clueView.setBackground(background);
                LinearLayout.LayoutParams clueParams = new LinearLayout.LayoutParams(
                        LinearLayout.LayoutParams.MATCH_PARENT,
                        LinearLayout.LayoutParams.WRAP_CONTENT);
                clueParams.bottomMargin = dp(2);
                clueContainer.addView(clueView, clueParams);
                clueView.setOnLongClickListener(view -> {
                    showThemedDialog(new AlertDialog.Builder(this)
                            .setTitle(clue.title)
                            .setMessage(clue.explanation)
                        .setPositiveButton(android.R.string.ok, null));
                    return true;
                });
            }
            clueContainer.post(this::fitQuestionToAvailableHeight);
            rangeView.setText("Choose a number from " + question.minimum + " to " + question.maximum);
            solutionCountView.setText(question.solutionCount +
                    (question.solutionCount == 1 ? " possible answer" : " possible answers"));
            if (game.getQuestionsAnswered() >= 10) {
                messageView.setVisibility(View.GONE);
            } else {
                messageView.setVisibility(View.VISIBLE);
                messageView.setText("Hold a rule for its definition.");
            }
                answerInput.setHint("Your answer");
            answerInput.setText("");
            answerInput.setEnabled(true);
            actionButton.setText("Submit answer");
            actionButton.setEnabled(true);
            updateStats();
            saveProgress();
        });
    }

    private void submitAnswer() {
        String answerText = answerInput.getText().toString().trim();
        try {
            int guess = Integer.parseInt(answerText);
            if (guess < currentMinimum || guess > currentMaximum) {
                messageView.setText("That number is outside the allowed range.");
                animateRangePrompt();
                return;
            }
        } catch (NumberFormatException ignored) {
            // The engine reports empty or malformed input without consuming a life.
        }
        int previousLives = game.getLives();
        NumberGameEngine.AnswerResult result = game.submitAnswer(answerText);
        updateStats();
        if (result.lives != previousLives) {
            animateLivesChange(previousLives, result.lives);
        }
        switch (result.status) {
            case INVALID:
                messageView.setText("Enter a whole number.");
                break;
            case WRONG:
                messageView.setText("Not quite. Try another number.");
                playTone(ToneGenerator.TONE_PROP_NACK, 170);
                answerInput.setText("");
                ObjectAnimator shake = ObjectAnimator.ofFloat(answerInput, "translationX",
                        0, dp(8), -dp(8), dp(6), -dp(6), 0);
                shake.setDuration(360);
                shake.start();
                animateRuleFeedback(result.clueMatches, false);
                saveProgress();
                break;
            case CORRECT:
                String message = "Correct. +" + result.pointsEarned + " points.";
                if (result.levelUp) {
                    message += " Level " + result.level + " unlocked. +1 life.";
                }
                messageView.setText(message);
                playTone(result.levelUp ? ToneGenerator.TONE_PROP_ACK : ToneGenerator.TONE_PROP_BEEP,
                    result.levelUp ? 420 : 120);
                showPointsEarned(result.pointsEarned);
                animateRuleFeedback(Collections.emptyList(), true);
                answerInput.setEnabled(false);
                actionButton.setText("Preparing question...");
                actionButton.setEnabled(false);
                saveProgress();
                maybeUpdateHighScore(result.totalPoints);
                new Handler(Looper.getMainLooper()).postDelayed(
                    () -> game.requestNextQuestion(this::showQuestion), 820);
                break;
            case GAME_OVER:
                gameOver = true;
                gameStarted = false;
                answerInput.setText("");
                clearSavedProgress();
                animateRuleFeedback(result.clueMatches, false);
                new Handler(Looper.getMainLooper()).postDelayed(() -> showThemedDialog(
                        new AlertDialog.Builder(this)
                                .setTitle("Game over")
                                .setMessage("One correct answer was " + result.correctAnswer
                                        + ".\n\nYou scored " + result.totalPoints + " points across "
                                        + game.getQuestionsAnswered() + " questions.")
                                .setPositiveButton("Return home",
                                        (dialog, which) -> resetHomeScreen())
                                .setCancelable(false)), 760);
                break;
            default:
                break;
        }
    }

    private void offerContinueIfSavedGame() {
        NumberGameEngine.GameSnapshot snapshot = loadSavedGame();
        if (snapshot == null) return;
        showThemedDialog(new AlertDialog.Builder(this)
                .setTitle("Game in progress")
                .setMessage("Continue your saved game?")
                .setPositiveButton("Continue", (dialog, which) -> {
                    gameStarted = true;
                    gameOver = false;
                    highScorePopupShown = getSharedPreferences(SETTINGS_FILE, MODE_PRIVATE)
                            .getBoolean(HIGH_SCORE_POPUP_KEY, false);
                    answerInput.setHint("Your answer");
                    answerInput.setEnabled(false);
                    actionButton.setText("Preparing question...");
                    actionButton.setEnabled(false);
                    messageView.setVisibility(View.VISIBLE);
                    messageView.setText("Game restored.");
                    game.restoreGame(snapshot, this::showQuestion);
                    updateStats();
                })
                .setNegativeButton("New game", (dialog, which) -> {
                    clearSavedProgress();
                    resetHomeScreen();
                })
                .setCancelable(false));
    }

    private NumberGameEngine.GameSnapshot loadSavedGame() {
        String encoded = getSharedPreferences(SETTINGS_FILE, MODE_PRIVATE)
                .getString(SAVED_GAME_KEY, null);
        if (encoded == null) return null;
        try (ObjectInputStream input = new ObjectInputStream(new ByteArrayInputStream(
                Base64.decode(encoded, Base64.DEFAULT)))) {
            return (NumberGameEngine.GameSnapshot) input.readObject();
        } catch (Exception exception) {
            clearSavedProgress();
            return null;
        }
    }

    private void saveProgress() {
        if (game == null) return;
        NumberGameEngine.GameSnapshot snapshot = game.createSnapshot();
        if (snapshot == null) return;
        try (ByteArrayOutputStream bytes = new ByteArrayOutputStream();
             ObjectOutputStream output = new ObjectOutputStream(bytes)) {
            output.writeObject(snapshot);
            output.flush();
            String encoded = Base64.encodeToString(bytes.toByteArray(), Base64.DEFAULT);
            getSharedPreferences(SETTINGS_FILE, MODE_PRIVATE).edit()
                    .putString(SAVED_GAME_KEY, encoded).apply();
        } catch (Exception ignored) {
            clearSavedProgress();
        }
    }

    private void clearSavedProgress() {
        getSharedPreferences(SETTINGS_FILE, MODE_PRIVATE).edit()
                .remove(SAVED_GAME_KEY).apply();
    }

    private void resetHomeScreen() {
        clearSavedProgress();
        getSharedPreferences(SETTINGS_FILE, MODE_PRIVATE).edit()
            .remove(HIGH_SCORE_POPUP_KEY).apply();
        if (game != null) game.close();
        game = new NumberGameEngine();
        gameStarted = false;
        gameOver = false;
        currentMinimum = 0;
        currentMaximum = 0;
        clueContainer.removeAllViews();
        rangeView.setText("");
        solutionCountView.setText("");
        messageView.setVisibility(View.VISIBLE);
        messageView.setText("");
        answerInput.setText("");
        answerInput.setHint("Seed (optional)");
        answerInput.setEnabled(true);
        actionButton.setText("Start game");
        actionButton.setEnabled(true);
        pointsOverlayView.animate().cancel();
        pointsOverlayView.setVisibility(View.GONE);
        updateStats();
    }

    private int readHighScore() {
        File file = new File(getFilesDir(), HIGH_SCORE_FILE);
        if (!file.isFile()) return 0;
        try (FileInputStream input = new FileInputStream(file)) {
            byte[] bytes = new byte[(int) Math.min(file.length(), 32)];
            int length = input.read(bytes);
            return length <= 0 ? 0 : Math.max(0,
                    Integer.parseInt(new String(bytes, 0, length, StandardCharsets.UTF_8).trim()));
        } catch (Exception ignored) {
            return 0;
        }
    }

    private void maybeUpdateHighScore(int points) {
        if (!gameStarted || !game.usesRandomSeed()) return;
        int previousHighScore = readHighScore();
        int newHighScore = Math.max(previousHighScore, points);
        try (FileOutputStream output = new FileOutputStream(
                new File(getFilesDir(), HIGH_SCORE_FILE), false)) {
            output.write(Integer.toString(newHighScore).getBytes(StandardCharsets.UTF_8));
            output.getFD().sync();
        } catch (Exception ignored) {
            return;
        }
        if (points > previousHighScore && !highScorePopupShown) {
            highScorePopupShown = true;
            getSharedPreferences(SETTINGS_FILE, MODE_PRIVATE).edit()
                    .putBoolean(HIGH_SCORE_POPUP_KEY, true).apply();
            showThemedDialog(new AlertDialog.Builder(this)
                    .setTitle("New high score")
                    .setMessage("Your new random-game high score is " + points + " points.")
                    .setPositiveButton(android.R.string.ok, null));
        }
    }

    private void animateRangePrompt() {
        ObjectAnimator shake = ObjectAnimator.ofFloat(rangeView, "translationX",
                0, dp(7), -dp(7), dp(5), -dp(5), 0);
        shake.setDuration(420);
        shake.start();
        int base = darkMode ? Color.rgb(230, 242, 238) : Color.rgb(32, 49, 46);
        int highlight = darkMode ? Color.rgb(255, 184, 112) : Color.rgb(190, 84, 49);
        ValueAnimator color = ValueAnimator.ofObject(new ArgbEvaluator(), base, highlight, base);
        color.addUpdateListener(animation -> rangeView.setTextColor((Integer) animation.getAnimatedValue()));
        color.setDuration(700);
        color.start();
    }

    private void animateRuleFeedback(List<Boolean> ruleMatches, boolean correct) {
        int base = darkMode ? Color.rgb(38, 58, 53) : Color.rgb(232, 242, 239);
        int border = darkMode ? Color.rgb(70, 96, 88) : Color.rgb(204, 224, 217);
        for (int index = 0; index < clueContainer.getChildCount(); index++) {
            View view = clueContainer.getChildAt(index);
            if (!(view instanceof TextView)) continue;
            boolean matched = correct || (index < ruleMatches.size() && ruleMatches.get(index));
            int target;
            if (correct) {
                target = darkMode ? Color.rgb(59, 128, 108) : Color.rgb(177, 226, 202);
            } else if (matched) {
                target = darkMode ? Color.rgb(46, 112, 82) : Color.rgb(180, 230, 192);
            } else {
                target = darkMode ? Color.rgb(132, 61, 61) : Color.rgb(246, 190, 181);
            }
            TextView clue = (TextView) view;
            clue.setTextColor(darkMode ? Color.rgb(245, 250, 248) : Color.rgb(32, 49, 46));
            ValueAnimator glow = ValueAnimator.ofFloat(0, 1, 0);
            glow.setDuration(760);
            glow.setInterpolator(new DecelerateInterpolator());
            glow.addUpdateListener(animation -> {
                int color = (Integer) new ArgbEvaluator().evaluate(
                        (Float) animation.getAnimatedValue(), base, target);
                clue.setBackground(buttonBackground(color, border));
            });
            glow.start();
            clue.animate().scaleX(1.025f).scaleY(1.025f).setDuration(160)
                    .withEndAction(() -> clue.animate().scaleX(1f).scaleY(1f)
                            .setDuration(240).start()).start();
        }
    }

    private void updateStats() {
        statsView.setText("Level " + game.getLevel() + "     " + game.getPoints() +
                " points");
        livesView.setText(game.getLives() + (game.getLives() == 1 ? " life" : " lives"));
    }

    private void fitQuestionToAvailableHeight() {
        int availableHeight = clueScrollView.getHeight();
        int availableWidth = clueScrollView.getWidth();
        if (availableHeight <= 0 || availableWidth <= 0 || clueContainer.getChildCount() == 0) {
            return;
        }

        int textSize = 14;
        int verticalPadding = 5;
        int contentHeight = measureClues(availableWidth);
        while (contentHeight > availableHeight && (textSize > 11 || verticalPadding > 1)) {
            if (textSize > 11) {
                textSize--;
            } else {
                verticalPadding--;
            }
            for (int index = 0; index < clueContainer.getChildCount(); index++) {
                View child = clueContainer.getChildAt(index);
                if (child instanceof TextView) {
                    TextView clueView = (TextView) child;
                    clueView.setTextSize(textSize);
                    clueView.setPadding(dp(8), dp(verticalPadding), dp(8), dp(verticalPadding));
                    LinearLayout.LayoutParams params = (LinearLayout.LayoutParams) child.getLayoutParams();
                    params.bottomMargin = dp(1);
                    child.setLayoutParams(params);
                }
            }
            contentHeight = measureClues(availableWidth);
        }
    }

    private int measureClues(int width) {
        clueContainer.measure(
                View.MeasureSpec.makeMeasureSpec(width, View.MeasureSpec.EXACTLY),
                View.MeasureSpec.makeMeasureSpec(0, View.MeasureSpec.UNSPECIFIED));
        return clueContainer.getMeasuredHeight();
    }

    private void restartGame() {
        if ((gameStarted || gameOver) && !game.usesRandomSeed()) {
            answerInput.setText(Long.toString(game.getCurrentSeed()));
        } else if (gameStarted || gameOver) {
            answerInput.setText("");
        }
        startGame();
    }

    private void applyPalette() {
        int background = darkMode ? Color.rgb(20, 33, 31) : Color.rgb(242, 247, 245);
        int clueSurface = darkMode ? Color.rgb(38, 58, 53) : Color.rgb(232, 242, 239);
        int primary = darkMode ? Color.rgb(83, 185, 168) : Color.rgb(25, 121, 111);
        int text = darkMode ? Color.rgb(230, 242, 238) : Color.rgb(32, 49, 46);
        int muted = darkMode ? Color.rgb(169, 192, 185) : Color.rgb(88, 112, 107);
        int keypadSurface = darkMode ? Color.rgb(47, 68, 62) : Color.rgb(225, 239, 235);
        int border = darkMode ? Color.rgb(70, 96, 88) : Color.rgb(204, 224, 217);

        gameRoot.setBackgroundColor(background);
        titleView.setTextColor(text);
        statsView.setTextColor(muted);
        livesView.setTextColor(muted);
        rangeView.setTextColor(text);
        solutionCountView.setTextColor(muted);
        messageView.setTextColor(muted);
        answerInput.setTextColor(text);
        answerInput.setHintTextColor(muted);
        settingsButton.setColorFilter(text);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            answerInput.setBackgroundTintList(ColorStateList.valueOf(muted));
            getWindow().setStatusBarColor(darkMode
                    ? Color.rgb(13, 24, 22) : Color.rgb(18, 83, 78));
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            getWindow().getDecorView().setSystemUiVisibility(darkMode
                    ? 0 : View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR);
        }
        if (getSupportActionBar() != null) {
            getSupportActionBar().setBackgroundDrawable(new ColorDrawable(
                    darkMode ? Color.rgb(24, 61, 56) : Color.rgb(25, 121, 111)));
        }

        int[] keypadIds = {R.id.btnDigit0, R.id.btnDigit1, R.id.btnDigit2,
                R.id.btnDigit3, R.id.btnDigit4, R.id.btnDigit5, R.id.btnDigit6,
                R.id.btnDigit7, R.id.btnDigit8, R.id.btnDigit9,
                R.id.btnBackspace, R.id.btnClear};
        for (int id : keypadIds) {
            Button button = findViewById(id);
            button.setTextColor(darkMode ? Color.rgb(245, 250, 248) : text);
            button.setBackground(buttonBackground(keypadSurface, border));
        }
        actionButton.setTextColor(Color.WHITE);
        actionButton.setBackground(buttonBackground(primary, darkMode
            ? Color.rgb(111, 205, 188) : Color.rgb(18, 96, 87)));
        pointsOverlayView.setBackground(buttonBackground(
            darkMode ? Color.rgb(188, 108, 72) : Color.rgb(185, 88, 52), border));

        for (int index = 0; index < clueContainer.getChildCount(); index++) {
            View child = clueContainer.getChildAt(index);
            if (child instanceof TextView) {
                ((TextView) child).setTextColor(text);
                child.setBackground(buttonBackground(clueSurface, border));
            }
        }
    }

    private GradientDrawable buttonBackground(int color, int border) {
        GradientDrawable background = new GradientDrawable();
        background.setColor(color);
        background.setCornerRadius(dp(5));
        background.setStroke(dp(1), border);
        return background;
    }

    private void animateLivesChange(int previousLives, int currentLives) {
        int highlight = currentLives > previousLives
                ? Color.rgb(70, 190, 153) : Color.rgb(229, 112, 91);
        int resting = darkMode ? Color.rgb(169, 192, 185) : Color.rgb(88, 112, 107);
        ObjectAnimator scaleX = ObjectAnimator.ofFloat(livesView, "scaleX", 1f, 1.3f, 1f);
        ObjectAnimator scaleY = ObjectAnimator.ofFloat(livesView, "scaleY", 1f, 1.3f, 1f);
        ObjectAnimator lift = ObjectAnimator.ofFloat(livesView, "translationY", 0,
                currentLives > previousLives ? -dp(5) : dp(5), 0);
        ValueAnimator color = ValueAnimator.ofObject(new ArgbEvaluator(), highlight, resting);
        color.addUpdateListener(animation -> livesView.setTextColor((Integer) animation.getAnimatedValue()));
        AnimatorSet animation = new AnimatorSet();
        animation.playTogether(scaleX, scaleY, lift, color);
        animation.setDuration(520);
        animation.start();
    }

    private void playTone(int tone, int durationMillis) {
        if (soundGenerator != null) {
            soundGenerator.startTone(tone, durationMillis);
        }
    }

    private void showPointsEarned(int points) {
        pointsOverlayView.animate().cancel();
        pointsOverlayView.setText("+" + points + " points");
        pointsOverlayView.setVisibility(View.VISIBLE);
        pointsOverlayView.setAlpha(0f);
        pointsOverlayView.setScaleX(0.8f);
        pointsOverlayView.setScaleY(0.8f);
        pointsOverlayView.setTranslationY(dp(12));
        pointsOverlayView.animate()
                .alpha(1f)
                .scaleX(1f)
                .scaleY(1f)
                .translationY(0)
                .setDuration(180)
                .withEndAction(() -> pointsOverlayView.animate()
                        .alpha(0f)
                        .translationY(-dp(18))
                        .setStartDelay(550)
                        .setDuration(400)
                        .withEndAction(() -> pointsOverlayView.setVisibility(View.GONE))
                        .start())
                .start();
    }

    private int dp(int value) {
        return (int) (value * getResources().getDisplayMetrics().density + 0.5f);
    }

    private void appendDigit(int digit) {
        if (!answerInput.isEnabled()) {
            return;
        }
        answerInput.append(Integer.toString(digit));
    }

    private void deleteLastDigit() {
        if (!answerInput.isEnabled()) {
            return;
        }
        String value = answerInput.getText().toString();
        if (!value.isEmpty()) {
            answerInput.setText(value.substring(0, value.length() - 1));
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (soundGenerator != null) {
            soundGenerator.release();
            soundGenerator = null;
        }
        if (game != null) {
            game.close();
        }
    }

    @Override
    protected void onPause() {
        if (gameStarted) {
            saveProgress();
        }
        super.onPause();
    }
}
