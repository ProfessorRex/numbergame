package com.numgame.python.console;

import java.io.Serializable;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Random;
import java.util.Set;

public final class NumberGameEngine implements AutoCloseable {
    public static final int FUTURE_QUESTION_LIMIT = 10;

    public interface QuestionListener {
        void onQuestionReady(Question question);
    }

    public enum AnswerStatus {
        CORRECT, WRONG, INVALID, GAME_OVER
    }

    public static final class AnswerResult {
        public final AnswerStatus status;
        public final int pointsEarned;
        public final int totalPoints;
        public final int lives;
        public final int level;
        public final boolean levelUp;
        public final Integer correctAnswer;
        public final List<Boolean> clueMatches;

        private AnswerResult(AnswerStatus status, int pointsEarned, int totalPoints,
                     int lives, int level, boolean levelUp, Integer correctAnswer,
                     List<Boolean> clueMatches) {
            this.status = status;
            this.pointsEarned = pointsEarned;
            this.totalPoints = totalPoints;
            this.lives = lives;
            this.level = level;
            this.levelUp = levelUp;
            this.correctAnswer = correctAnswer;
            this.clueMatches = Collections.unmodifiableList(new ArrayList<>(clueMatches));
        }
    }

    public static final class Clue implements Serializable {
        private static final long serialVersionUID = 1L;
        public final String text;
        public final String title;
        public final String explanation;

        private Clue(String text, String title, String explanation) {
            this.text = text;
            this.title = title;
            this.explanation = explanation;
        }
    }

    public static final class Question implements Serializable {
        private static final long serialVersionUID = 1L;
        public final List<Clue> clues;
        public final int minimum;
        public final int maximum;
        public final int solutionCount;
        private final List<Integer> solutions;
        private final List<Rule> rules;
        private final List<Integer> ruleParameters;
        private final String signature;

        private Question(List<Clue> clues, int minimum, int maximum,
                 List<Integer> solutions, List<Rule> rules,
                 List<Integer> ruleParameters,
                 String signature) {
            this.clues = Collections.unmodifiableList(new ArrayList<>(clues));
            this.minimum = minimum;
            this.maximum = maximum;
            this.solutions = Collections.unmodifiableList(new ArrayList<>(solutions));
            this.rules = Collections.unmodifiableList(new ArrayList<>(rules));
            this.ruleParameters = Collections.unmodifiableList(new ArrayList<>(ruleParameters));
            this.solutionCount = solutions.size();
            this.signature = signature;
        }

        private List<Boolean> matchesFor(int number, NumberGameEngine engine) {
            List<Boolean> matches = new ArrayList<>();
            for (int index = 0; index < rules.size(); index++) {
                matches.add(engine.matches(rules.get(index), number, ruleParameters.get(index)));
            }
            return matches;
        }
    }

    public static final class GameSnapshot implements Serializable {
        private static final long serialVersionUID = 1L;
        private final int level;
        private final int lives;
        private final int points;
        private final int questionsAnswered;
        private final int generatedQuestionCount;
        private final long currentSeed;
        private final long elapsedMillis;
        private final boolean randomSeed;
        private final Random random;
        private final ArrayDeque<Question> futureQuestions;
        private final Set<String> seenQuestions;
        private final Question currentQuestion;

        private GameSnapshot(int level, int lives, int points, int questionsAnswered,
                     int generatedQuestionCount,
                             long currentSeed, long elapsedMillis, boolean randomSeed,
                             Random random, ArrayDeque<Question> futureQuestions,
                             Set<String> seenQuestions, Question currentQuestion) {
            this.level = level;
            this.lives = lives;
            this.points = points;
            this.questionsAnswered = questionsAnswered;
            this.generatedQuestionCount = generatedQuestionCount;
            this.currentSeed = currentSeed;
            this.elapsedMillis = elapsedMillis;
            this.randomSeed = randomSeed;
            this.random = random;
            this.futureQuestions = futureQuestions;
            this.seenQuestions = seenQuestions;
            this.currentQuestion = currentQuestion;
        }
    }

    private enum Rule {
        EVEN(1), ODD(1), DIGIT_SUM(1), CYCLOPS(3), INCREASING(1), NUDE(2),
        DECREASING(1), EVENISH(1), ODDISH(1), BAN(1),
        PRIME(2), COMPOSITE(2), ALTERNATING(2), UNDULATING(2), PALINDROME(2),
        TWIN_PRIME(2), DIGIT_PRODUCT(2),
        NON_TRIVIAL_ALTERNATING(3), NON_TRIVIAL_UNDULATING(3), SEMIPRIME(3),
        INTERPRIME(3), NON_TRIVIAL_PALINDROME(3), STRICTLY_DECREASING(3),
        STRICTLY_INCREASING(3),
        NIVEN(4), NARCISSISTIC(4), EMIRP(4), EMIRPIMES(4), EMIRPRETNI(4),
        MORAN(5);

        final int unlockLevel;

        Rule(int unlockLevel) {
            this.unlockLevel = unlockLevel;
        }
    }

    private static final int[] MAXIMUMS = {100, 100, 1000, 1000, 10000, 10000, 10000};
    private static final int[] MINIMUMS = {0, 0, 10, 10, 100, 1000, 1000};
    private static final int[] LEVEL_THRESHOLDS = {0, 50, 200, 600, 1500, 3000};
    private static final char[] BAN_LETTERS = {'a', 'e', 'i', 'o', 't', 'u'};

    private final Object monitor = new Object();
    private Random random = new Random();
    private final ArrayDeque<Question> futureQuestions = new ArrayDeque<>();
    private final Set<String> seenQuestions = new HashSet<>();
    private final Thread generatorThread;
    private int level = 1;
    private int lives = 3;
    private int points;
    private int questionsAnswered;
    private int generatedQuestionCount;
    private long currentSeed;
    private boolean randomSeed;
    private long questionStartedAt;
    private long generationEpoch;
    private boolean running;
    private boolean closed;
    private Question currentQuestion;
    private QuestionListener pendingListener;

    public NumberGameEngine() {
        generatorThread = new Thread(this::generateInBackground, "number-game-generator");
        generatorThread.setDaemon(true);
        generatorThread.start();
    }

    public void startGame(int startLevel, QuestionListener listener) {
        startGame(startLevel, null, listener);
    }

    public void startGame(int startLevel, Long seed, QuestionListener listener) {
        synchronized (monitor) {
            level = Math.max(1, Math.min(6, startLevel));
            randomSeed = seed == null;
            currentSeed = seed == null ? new Random().nextLong() : seed;
            random = new Random(currentSeed);
            lives = 3;
            points = 0;
            questionsAnswered = 0;
            generatedQuestionCount = 0;
            currentQuestion = null;
            pendingListener = listener;
            running = true;
            futureQuestions.clear();
            seenQuestions.clear();
            generationEpoch++;
            monitor.notifyAll();
        }
    }

    public void restoreGame(GameSnapshot snapshot, QuestionListener listener) {
        synchronized (monitor) {
            level = snapshot.level;
            lives = snapshot.lives;
            points = snapshot.points;
            questionsAnswered = snapshot.questionsAnswered;
            generatedQuestionCount = snapshot.generatedQuestionCount;
            currentSeed = snapshot.currentSeed;
            randomSeed = snapshot.randomSeed;
            random = snapshot.random;
            futureQuestions.clear();
            futureQuestions.addAll(snapshot.futureQuestions);
            seenQuestions.clear();
            seenQuestions.addAll(snapshot.seenQuestions);
            currentQuestion = snapshot.currentQuestion;
            running = true;
            pendingListener = listener;
            if (currentQuestion != null) {
                questionStartedAt = System.currentTimeMillis() - snapshot.elapsedMillis;
                Question restoredQuestion = currentQuestion;
                pendingListener = null;
                listener.onQuestionReady(restoredQuestion);
            } else {
                deliverQuestionIfReady();
            }
            generationEpoch++;
            monitor.notifyAll();
        }
    }

    public GameSnapshot createSnapshot() {
        synchronized (monitor) {
            if (!running) {
                return null;
            }
            long elapsed = currentQuestion == null ? 0
                    : Math.max(0, System.currentTimeMillis() - questionStartedAt);
                return new GameSnapshot(level, lives, points, questionsAnswered,
                    generatedQuestionCount, currentSeed,
                    elapsed, randomSeed, random, new ArrayDeque<>(futureQuestions),
                    new HashSet<>(seenQuestions), currentQuestion);
        }
    }

    public boolean usesRandomSeed() {
        synchronized (monitor) {
            return randomSeed;
        }
    }

    public void requestNextQuestion(QuestionListener listener) {
        synchronized (monitor) {
            if (!running || closed) {
                return;
            }
            pendingListener = listener;
            deliverQuestionIfReady();
            monitor.notifyAll();
        }
    }

    public AnswerResult submitAnswer(String answer) {
        final int guess;
        try {
            guess = Integer.parseInt(answer.trim());
        } catch (RuntimeException exception) {
            return result(AnswerStatus.INVALID, 0, false);
        }

        synchronized (monitor) {
            if (!running || currentQuestion == null) {
                return result(AnswerStatus.INVALID, 0, false);
            }
            if (!currentQuestion.solutions.contains(guess)) {
                List<Boolean> clueMatches = currentQuestion.matchesFor(guess, this);
                lives--;
                if (lives <= 0) {
                    int correctAnswer = currentQuestion.solutions.get(0);
                    running = false;
                    currentQuestion = null;
                    futureQuestions.clear();
                    generationEpoch++;
                    monitor.notifyAll();
                    return result(AnswerStatus.GAME_OVER, 0, false, correctAnswer, clueMatches);
                }
                return result(AnswerStatus.WRONG, 0, false, null, clueMatches);
            }

            int earned = calculatePoints(guess, currentQuestion, level,
                    (System.currentTimeMillis() - questionStartedAt) / 1000.0);
            points += earned;
            questionsAnswered++;
            currentQuestion = null;
            boolean levelUp = level < 6 && points >= LEVEL_THRESHOLDS[level];
            if (levelUp) {
                level++;
                lives++;
                generatedQuestionCount -= futureQuestions.size();
                futureQuestions.clear();
                generationEpoch++;
            }
            monitor.notifyAll();
            return result(AnswerStatus.CORRECT, earned, levelUp);
        }
    }

    public int getLevel() {
        synchronized (monitor) {
            return level;
        }
    }

    public int getLives() {
        synchronized (monitor) {
            return lives;
        }
    }

    public int getPoints() {
        synchronized (monitor) {
            return points;
        }
    }

    public int getQuestionsAnswered() {
        synchronized (monitor) {
            return questionsAnswered;
        }
    }

    public long getCurrentSeed() {
        synchronized (monitor) {
            return currentSeed;
        }
    }

    public int getQueuedQuestionCount() {
        synchronized (monitor) {
            return futureQuestions.size();
        }
    }

    private AnswerResult result(AnswerStatus status, int earned, boolean levelUp) {
        return result(status, earned, levelUp, null, Collections.emptyList());
    }

    private AnswerResult result(AnswerStatus status, int earned, boolean levelUp,
                                Integer correctAnswer, List<Boolean> clueMatches) {
        return new AnswerResult(status, earned, points, lives, level, levelUp,
                correctAnswer, clueMatches);
    }

    private void generateInBackground() {
        while (true) {
            int requestedLevel;
            long requestedEpoch;
            Random requestedRandom;
            boolean requireDigitHint;
            Set<String> history;
            synchronized (monitor) {
                while (!closed && (!running || futureQuestions.size() >= FUTURE_QUESTION_LIMIT)) {
                    try {
                        monitor.wait();
                    } catch (InterruptedException exception) {
                        if (closed) {
                            return;
                        }
                    }
                }
                if (closed) {
                    return;
                }
                requestedLevel = level;
                requestedEpoch = generationEpoch;
                requestedRandom = random;
                requireDigitHint = generatedQuestionCount % 2 == 0;
                history = new HashSet<>(seenQuestions);
            }

            Question question = createQuestion(requestedLevel, history, requestedRandom,
                    requireDigitHint);
            synchronized (monitor) {
                if (!running || closed || requestedEpoch != generationEpoch || requestedLevel != level) {
                    continue;
                }
                if (!seenQuestions.add(question.signature)) {
                    continue;
                }
                futureQuestions.addLast(question);
                generatedQuestionCount++;
                deliverQuestionIfReady();
                monitor.notifyAll();
            }
        }
    }

    private void deliverQuestionIfReady() {
        if (pendingListener == null || futureQuestions.isEmpty() || !running) {
            return;
        }
        Question question = futureQuestions.removeFirst();
        currentQuestion = question;
        questionStartedAt = System.currentTimeMillis();
        QuestionListener listener = pendingListener;
        pendingListener = null;
        listener.onQuestionReady(question);
    }

    private Question createQuestion(int requestedLevel, Set<String> history,
                                    Random sourceRandom, boolean requireDigitHint) {
        List<Rule> unlocked = new ArrayList<>();
        for (Rule rule : Rule.values()) {
            if (rule.unlockLevel <= requestedLevel) {
                unlocked.add(rule);
            }
        }

        while (true) {
            int maximum = MAXIMUMS[sourceRandom.nextInt(requestedLevel + 1)];
            List<Integer> validMinimums = new ArrayList<>();
            for (int index = 0; index <= requestedLevel; index++) {
                if (MINIMUMS[index] < maximum) {
                    validMinimums.add(MINIMUMS[index]);
                }
            }
            int minimum = validMinimums.get(sourceRandom.nextInt(validMinimums.size()));
                List<Rule> selected = sampleRules(unlocked, sourceRandom,
                    requireDigitHint, requestedLevel);
            if (hasExclusion(selected)) {
                continue;
            }

            List<Integer> possible = new ArrayList<>();
            for (int number = minimum; number <= maximum; number++) {
                possible.add(number);
            }
            List<Clue> clues = new ArrayList<>();
            List<Rule> questionRules = new ArrayList<>();
            List<Integer> ruleParameters = new ArrayList<>();
            java.util.Map<Rule, Integer> parameters = new java.util.EnumMap<>(Rule.class);
            boolean hasSolutions = true;
            for (Rule rule : selected) {
                if (rule == Rule.DIGIT_SUM || rule == Rule.DIGIT_PRODUCT) {
                    continue;
                }
                int parameter = 0;
                if (rule == Rule.BAN) {
                    List<Character> availableLetters = new ArrayList<>();
                    for (char letter : BAN_LETTERS) {
                        boolean hasCandidate = false;
                        for (int candidate : possible) {
                            if (numberToEnglish(candidate).toLowerCase(Locale.US).indexOf(letter) < 0) {
                                hasCandidate = true;
                                break;
                            }
                        }
                        if (hasCandidate) {
                            availableLetters.add(letter);
                        }
                    }
                    if (availableLetters.isEmpty()) {
                        hasSolutions = false;
                        break;
                    }
                    parameter = availableLetters.get(sourceRandom.nextInt(availableLetters.size()));
                }
                parameters.put(rule, parameter);

                final int clueParameter = parameter;
                List<Integer> filtered = new ArrayList<>();
                for (int number : possible) {
                    if (matches(rule, number, clueParameter)) {
                        filtered.add(number);
                    }
                }
                possible = filtered;
                if (possible.isEmpty()) {
                    hasSolutions = false;
                    break;
                }
            }
            if (!hasSolutions) {
                continue;
            }

            List<Rule> arithmeticRules = new ArrayList<>();
            for (Rule rule : selected) {
                if (rule == Rule.DIGIT_SUM || rule == Rule.DIGIT_PRODUCT) {
                    arithmeticRules.add(rule);
                }
            }
            if (!arithmeticRules.isEmpty()) {
                int answerForHints = possible.get(sourceRandom.nextInt(possible.size()));
                for (Rule rule : arithmeticRules) {
                    parameters.put(rule, rule == Rule.DIGIT_SUM
                            ? digitSum(answerForHints) : digitProduct(answerForHints));
                    List<Integer> filtered = new ArrayList<>();
                    int parameter = parameters.get(rule);
                    for (int number : possible) {
                        if (matches(rule, number, parameter)) {
                            filtered.add(number);
                        }
                    }
                    possible = filtered;
                }
                if (possible.isEmpty()) {
                    continue;
                }
            }
            for (Rule rule : selected) {
                int parameter = parameters.get(rule);
                clues.add(makeClue(rule, parameter, sourceRandom));
                questionRules.add(rule);
                ruleParameters.add(parameter);
            }
            if (!hasSolutions) {
                continue;
            }

            String signature = signature(requestedLevel, minimum, maximum, clues);
            if (history.contains(signature)) {
                continue;
            }
                return new Question(clues, minimum, maximum, possible,
                    questionRules, ruleParameters, signature);
        }
    }

    private List<Rule> sampleRules(List<Rule> unlocked, Random sourceRandom,
                                   boolean requireDigitHint, int currentLevel) {
        List<Rule> pool = new ArrayList<>(unlocked);
        List<Rule> selected = new ArrayList<>(3);
        if (requireDigitHint) {
            List<Rule> arithmetic = new ArrayList<>();
            for (Rule rule : pool) {
                if (rule == Rule.DIGIT_SUM || rule == Rule.DIGIT_PRODUCT) {
                    arithmetic.add(rule);
                }
            }
            Rule picked = weightedRule(arithmetic, sourceRandom, currentLevel);
            selected.add(picked);
            pool.remove(picked);
        } else {
            pool.remove(Rule.DIGIT_SUM);
            pool.remove(Rule.DIGIT_PRODUCT);
        }
        while (selected.size() < 3) {
            Rule picked = weightedRule(pool, sourceRandom, currentLevel);
            selected.add(picked);
            pool.remove(picked);
        }
        return selected;
    }

    private Rule weightedRule(List<Rule> pool, Random sourceRandom, int currentLevel) {
        int totalWeight = 0;
        for (Rule rule : pool) {
            totalWeight += rule == Rule.DIGIT_SUM || rule == Rule.DIGIT_PRODUCT
                    ? (currentLevel <= 2 ? 6 : 3) : 1;
        }
        int choice = sourceRandom.nextInt(totalWeight);
        for (Rule rule : pool) {
            choice -= rule == Rule.DIGIT_SUM || rule == Rule.DIGIT_PRODUCT
                    ? (currentLevel <= 2 ? 6 : 3) : 1;
            if (choice < 0) return rule;
        }
        return pool.get(pool.size() - 1);
    }

    private boolean hasExclusion(List<Rule> selected) {
        return conflicts(selected, Rule.EVEN, Rule.ODD)
                || conflicts(selected, Rule.EVENISH, Rule.ODDISH)
                || conflicts(selected, Rule.DIGIT_SUM, Rule.EVENISH)
                || conflicts(selected, Rule.DIGIT_SUM, Rule.ODDISH)
                || conflicts(selected, Rule.INCREASING, Rule.STRICTLY_INCREASING)
                || conflicts(selected, Rule.DECREASING, Rule.STRICTLY_DECREASING)
                || conflicts(selected, Rule.ALTERNATING, Rule.NON_TRIVIAL_ALTERNATING)
                || conflicts(selected, Rule.UNDULATING, Rule.NON_TRIVIAL_UNDULATING)
                || conflicts(selected, Rule.PALINDROME, Rule.NON_TRIVIAL_PALINDROME)
                || conflicts(selected, Rule.NIVEN, Rule.MORAN)
                || conflicts(selected, Rule.PRIME, Rule.EMIRP)
                || conflicts(selected, Rule.PRIME, Rule.TWIN_PRIME)
                || conflicts(selected, Rule.SEMIPRIME, Rule.EMIRPIMES)
                || conflicts(selected, Rule.INTERPRIME, Rule.EMIRPRETNI)
                || conflicts(selected, Rule.COMPOSITE, Rule.DIGIT_PRODUCT)
                || ((selected.contains(Rule.PRIME) || selected.contains(Rule.EMIRP)
                    || selected.contains(Rule.TWIN_PRIME))
                    && (selected.contains(Rule.SEMIPRIME) || selected.contains(Rule.EMIRPIMES)
                    || selected.contains(Rule.INTERPRIME) || selected.contains(Rule.EMIRPRETNI)));
    }

    private boolean conflicts(List<Rule> rules, Rule first, Rule second) {
        return rules.contains(first) && rules.contains(second);
    }

    private boolean matches(Rule rule, int number, int parameter) {
        switch (rule) {
            case EVEN: return number % 2 == 0;
            case ODD: return number % 2 != 0;
            case DIGIT_SUM: return digitSum(number) == parameter;
            case CYCLOPS: return isCyclops(number);
            case INCREASING: return isMonotonic(number, true, false);
            case NUDE: return isNude(number);
            case DECREASING: return isMonotonic(number, false, false);
            case EVENISH: return digitSum(number) % 2 == 0;
            case ODDISH: return digitSum(number) % 2 != 0;
            case BAN: return numberToEnglish(number).toLowerCase(Locale.US).indexOf(parameter) < 0;
            case PRIME: return isPrime(number);
            case COMPOSITE: return number > 1 && !isPrime(number);
            case ALTERNATING: return isAlternating(number);
            case UNDULATING: return isUndulating(number);
            case PALINDROME: return isPalindrome(number);
            case TWIN_PRIME: return isPrime(number) && (isPrime(number - 2) || isPrime(number + 2));
            case DIGIT_PRODUCT: return digitProduct(number) == parameter;
            case NON_TRIVIAL_ALTERNATING: return number >= 10 && isAlternating(number);
            case NON_TRIVIAL_UNDULATING: return number >= 101 && isNonTrivialUndulating(number);
            case SEMIPRIME: return isSemiprime(number);
            case INTERPRIME: return isInterprime(number);
            case NON_TRIVIAL_PALINDROME: return number >= 10 && isPalindrome(number);
            case STRICTLY_DECREASING: return isMonotonic(number, false, true);
            case STRICTLY_INCREASING: return isMonotonic(number, true, true);
            case NIVEN: return number > 0 && number % digitSum(number) == 0;
            case NARCISSISTIC: return isNarcissistic(number);
            case EMIRP: return isEmirp(number);
            case EMIRPIMES: return isEmirpimes(number);
            case EMIRPRETNI: return isEmirpretni(number);
            case MORAN:
                if (number == 0) return false;
                int sum = digitSum(number);
                return number % sum == 0 && isPrime(number / sum);
            default: return false;
        }
    }

    private Clue makeClue(Rule rule, int parameter, Random sourceRandom) {
        switch (rule) {
            case EVEN:
                return sourceRandom.nextInt(4) == 0
                        ? clue("X is not an odd number", "Even number", "A number evenly divisible by 2. Examples: 0, 2, 10, 108, 784.")
                        : clue("X is an Even Number", "Even number", "A number evenly divisible by 2. Examples: 0, 2, 10, 108, 784.");
            case ODD:
                return sourceRandom.nextInt(4) == 0
                        ? clue("X is not an even number", "Odd number", "A number not evenly divisible by 2. Examples: 1, 7, 13, 91, 999.")
                        : clue("X is an Odd Number", "Odd number", "A number not evenly divisible by 2. Examples: 1, 7, 13, 91, 999.");
            case DIGIT_SUM:
                return clue("The sum of X's digits is " + parameter, "Digit sum", "Add the number's individual digits. For example, 763 has digit sum 7 + 6 + 3 = 16.");
            case DIGIT_PRODUCT:
                return clue("The product of X's digits is " + parameter, "Digit product", "Multiply the number's individual digits. For example, 721 has digit product 7 x 2 x 1 = 14.");
            case BAN:
                String article = "tu".indexOf(parameter) >= 0 ? "a " : "an ";
                String explanation = "The English spelling of the number contains no letter '"
                        + (char) parameter + "'.";
                if (parameter == 'a') {
                    explanation += " Ignore the word 'and'.";
                }
                return clue("X is " + article + (char) parameter + "ban number in English",
                        ((char) parameter) + "ban number", explanation);
            case PRIME: return clue("X is a prime number", "Prime number", "A number greater than 1 with exactly two positive divisors: 1 and itself. For example, 13.");
            case COMPOSITE: return clue("X is a composite number", "Composite number", "An integer greater than 1 that is not prime; it can be written as a product of primes. For example, 22 = 2 x 11.");
            case CYCLOPS: return clue("X is a cyclops number", "Cyclops number", "A number with exactly one zero digit, positioned in the middle. Examples: 0, 102, 505, 81047.");
            case INCREASING: return clue("X is an increasing number", "Increasing number", "Each digit is greater than or equal to its predecessor, reading left to right. Examples: 9, 77, 223.");
            case DECREASING: return clue("X is a decreasing Number", "Decreasing number", "Each digit is less than or equal to its predecessor, reading left to right. Examples: 6, 333, 322.");
            case STRICTLY_INCREASING: return clue("X is a strictly increasing number", "Strictly increasing number", "Each digit is greater than its predecessor, reading left to right. Examples: 9, 158.");
            case STRICTLY_DECREASING: return clue("X is a strictly decreasing number", "Strictly decreasing number", "Each digit is less than its predecessor, reading left to right. Examples: 6, 321.");
            case EVENISH: return clue("X is an evenish number", "Evenish number", "The sum of the number's digits is even. For example, 42 has digit sum 6.");
            case ODDISH: return clue("X is an oddish number", "Oddish number", "The sum of the number's digits is odd. For example, 300 has digit sum 3.");
            case ALTERNATING: return clue("X is an alternating number", "Alternating number", "The parity of each digit switches between even and odd from left to right. Single-digit numbers are alternating.");
            case NON_TRIVIAL_ALTERNATING: return clue("X is a non-trivial alternating number", "Non-trivial alternating number", "An alternating number with at least two digits.");
            case UNDULATING: return clue("X is an undulating number", "Undulating number", "The digits repeat the pattern ABABAB...; A and B may be equal. Single-digit numbers are undulating.");
            case NON_TRIVIAL_UNDULATING: return clue("X is a non-trivial undulating number", "Non-trivial undulating number", "An undulating number with at least three digits and different repeating digits A and B.");
            case PALINDROME: return clue("X is a palindrome", "Palindrome", "The number reads the same forwards and backwards. Single-digit numbers are palindromes.");
            case NON_TRIVIAL_PALINDROME: return clue("X is a non-trivial palindrome", "Non-trivial palindrome", "A palindrome with at least two digits.");
            case TWIN_PRIME: return clue("X is a twin prime number", "Twin-prime number", "A prime with another prime exactly 2 away. For example, 17 and 19 form a twin-prime pair.");
            case SEMIPRIME: return clue("X is a semiprime number", "Semiprime number", "A number whose prime factorization contains exactly two prime factors, counted with multiplicity. Examples: 4 = 2 x 2; 247 = 13 x 19.");
            case EMIRP: return clue("X is an emirp", "Emirp", "A prime which becomes a different prime when its digits are reversed. For example, 13 reverses to 31; 11 is not an emirp.");
            case EMIRPIMES: return clue("X is an emirpimes number", "Emirpimes number", "A semiprime which becomes a different semiprime when its digits are reversed. For example, 15 reverses to 51.");
            case INTERPRIME: return clue("X is an interprime number", "Interprime number", "A composite number equally distant from the nearest prime below and above it. For example, 12 is between 11 and 13.");
            case EMIRPRETNI: return clue("X is an emirpretni number", "Emirpretni number", "An interprime whose reversed digits form a different interprime. Numbers ending in 0 cannot qualify.");
            case NIVEN: return clue("X is a niven (Harshad) number", "Niven (Harshad) number", "A number evenly divisible by its digit sum. For example, 133 has digit sum 7 and is divisible by 7.");
            case NUDE: return clue("X is a nude number", "Nude number", "A number evenly divisible by every one of its digits. A number containing 0 does not qualify.");
            case MORAN: return clue("X is a Moran number", "Moran number", "A Niven number whose quotient when divided by its digit sum is prime. For example, 18 / 9 = 2.");
            case NARCISSISTIC: return clue("X is a narcissistic (Armstrong) number", "Narcissistic (Armstrong) number", "A number equal to the sum of each digit raised to the number of digits. For example, 370 = 3^3 + 7^3 + 0^3.");
            default: return clue(rule.name(), rule.name(), rule.name());
        }
    }

    private Clue clue(String text, String title, String explanation) {
        return new Clue(text, title, explanation);
    }

    private String signature(int currentLevel, int minimum, int maximum, List<Clue> clues) {
        StringBuilder builder = new StringBuilder().append(currentLevel).append(':')
                .append(minimum).append(':').append(maximum);
        for (Clue clue : clues) {
            builder.append('|').append(clue.text);
        }
        return builder.toString();
    }

    private int calculatePoints(int answer, Question question, int currentLevel, double seconds) {
        List<Integer> ruleLevels = new ArrayList<>();
        for (Clue clue : question.clues) {
            ruleLevels.add(ruleLevel(clue.title));
        }
        Collections.sort(ruleLevels, Collections.reverseOrder());
        double ruleValue = 1.0;
        for (int index = 0; index < ruleLevels.size(); index++) {
            double factor = ruleLevels.get(index) * (ruleLevels.size() - index)
                    / (double) ruleLevels.size();
            ruleValue *= Math.max(1.0, factor);
        }
        double timeModifier = seconds <= 5 ? 3.0
                : Math.max(0.5, Math.min(Math.pow(0.97, seconds - 5) + 1,
                Math.pow(0.99, seconds - 77)));
        double solutionsModifier;
        if (question.solutionCount == 1) {
            solutionsModifier = 3.0;
        } else if (question.solutionCount == 2) {
            solutionsModifier = 2.0;
        } else {
            solutionsModifier = 1.0 + 1.0 / Math.sqrt(question.solutionCount);
        }
        double answerModifier = Math.max(1.0,
                Math.min(Math.pow(answer, 0.25), answer / 216.0 + 1.0));
        return 2 * (int) Math.ceil(answerModifier * ruleValue * timeModifier * solutionsModifier);
    }

    private int ruleLevel(String title) {
        for (Rule rule : Rule.values()) {
            if (makeClueTitle(rule).equals(title)) {
                return rule.unlockLevel;
            }
        }
        return 1;
    }

    private String makeClueTitle(Rule rule) {
        switch (rule) {
            case EVEN: return "Even number";
            case ODD: return "Odd number";
            case DIGIT_SUM: return "Digit sum";
            case CYCLOPS: return "Cyclops number";
            case INCREASING: return "Increasing number";
            case NUDE: return "Nude number";
            case DECREASING: return "Decreasing number";
            case EVENISH: return "Evenish number";
            case ODDISH: return "Oddish number";
            case BAN: return "aban number";
            case PRIME: return "Prime number";
            case COMPOSITE: return "Composite number";
            case ALTERNATING: return "Alternating number";
            case UNDULATING: return "Undulating number";
            case PALINDROME: return "Palindrome";
            case TWIN_PRIME: return "Twin-prime number";
            case DIGIT_PRODUCT: return "Digit product";
            case NON_TRIVIAL_ALTERNATING: return "Non-trivial alternating number";
            case NON_TRIVIAL_UNDULATING: return "Non-trivial undulating number";
            case SEMIPRIME: return "Semiprime number";
            case INTERPRIME: return "Interprime number";
            case NON_TRIVIAL_PALINDROME: return "Non-trivial palindrome";
            case STRICTLY_DECREASING: return "Strictly decreasing number";
            case STRICTLY_INCREASING: return "Strictly increasing number";
            case NIVEN: return "Niven (Harshad) number";
            case NARCISSISTIC: return "Narcissistic (Armstrong) number";
            case EMIRP: return "Emirp";
            case EMIRPIMES: return "Emirpimes number";
            case EMIRPRETNI: return "Emirpretni number";
            case MORAN: return "Moran number";
            default: return rule.name();
        }
    }

    private boolean isPrime(int number) {
        if (number < 2) return false;
        if (number % 2 == 0) return number == 2;
        for (int factor = 3; factor * factor <= number; factor += 2) {
            if (number % factor == 0) return false;
        }
        return true;
    }

    private boolean isSemiprime(int number) {
        if (number < 4) return false;
        int factorCount = 0;
        for (int factor = 2; factor * factor <= number; factor++) {
            while (number % factor == 0) {
                number /= factor;
                factorCount++;
                if (factorCount > 2) return false;
            }
        }
        if (number > 1) factorCount++;
        return factorCount == 2;
    }

    private boolean isInterprime(int number) {
        if (number <= 1 || isPrime(number)) return false;
        int lower = number - 1;
        while (lower > 1 && !isPrime(lower)) lower--;
        int upper = number + 1;
        while (!isPrime(upper)) upper++;
        return number - lower == upper - number;
    }

    private boolean isEmirp(int number) {
        int reversed = reverse(number);
        return reversed != number && isPrime(number) && isPrime(reversed);
    }

    private boolean isEmirpimes(int number) {
        int reversed = reverse(number);
        return reversed != number && isSemiprime(number) && isSemiprime(reversed);
    }

    private boolean isEmirpretni(int number) {
        int reversed = reverse(number);
        return number % 10 != 0 && reversed != number
                && isInterprime(number) && isInterprime(reversed);
    }

    private int reverse(int number) {
        int reversed = 0;
        while (number > 0) {
            reversed = reversed * 10 + number % 10;
            number /= 10;
        }
        return reversed;
    }

    private boolean isCyclops(int number) {
        if (number == 0) return true;
        String digits = Integer.toString(number);
        if (digits.length() % 2 == 0) return false;
        int zeroCount = 0;
        for (int index = 0; index < digits.length(); index++) {
            if (digits.charAt(index) == '0') {
                zeroCount++;
                if (index != digits.length() / 2) return false;
            }
        }
        return zeroCount == 1;
    }

    private boolean isNude(int number) {
        if (number == 0) return false;
        int remaining = number;
        while (remaining > 0) {
            int digit = remaining % 10;
            if (digit == 0 || number % digit != 0) return false;
            remaining /= 10;
        }
        return true;
    }

    private boolean isMonotonic(int number, boolean increasing, boolean strict) {
        String digits = Integer.toString(number);
        for (int index = 1; index < digits.length(); index++) {
            int previous = digits.charAt(index - 1) - '0';
            int current = digits.charAt(index) - '0';
            if (increasing) {
                if (strict ? current <= previous : current < previous) return false;
            } else if (strict ? current >= previous : current > previous) {
                return false;
            }
        }
        return true;
    }

    private boolean isAlternating(int number) {
        String digits = Integer.toString(number);
        for (int index = 1; index < digits.length(); index++) {
            if (((digits.charAt(index) - '0') & 1) == ((digits.charAt(index - 1) - '0') & 1)) {
                return false;
            }
        }
        return true;
    }

    private boolean isUndulating(int number) {
        String digits = Integer.toString(number);
        if (digits.length() < 3) return true;
        char first = digits.charAt(0);
        char second = digits.charAt(1);
        for (int index = 2; index < digits.length(); index++) {
            if (digits.charAt(index) != ((index & 1) == 0 ? first : second)) return false;
        }
        return true;
    }

    private boolean isNonTrivialUndulating(int number) {
        String digits = Integer.toString(number);
        return digits.length() >= 3 && digits.charAt(0) != digits.charAt(1)
                && isUndulating(number);
    }

    private boolean isPalindrome(int number) {
        String digits = Integer.toString(number);
        return digits.contentEquals(new StringBuilder(digits).reverse());
    }

    private boolean isNarcissistic(int number) {
        String digits = Integer.toString(number);
        int total = 0;
        for (int index = 0; index < digits.length(); index++) {
            total += (int) Math.pow(digits.charAt(index) - '0', digits.length());
        }
        return total == number;
    }

    private int digitSum(int number) {
        int total = 0;
        do {
            total += number % 10;
            number /= 10;
        } while (number > 0);
        return total;
    }

    private int digitProduct(int number) {
        int product = 1;
        do {
            product *= number % 10;
            number /= 10;
        } while (number > 0);
        return product;
    }

    private String numberToEnglish(int number) {
        if (number < 20) return SMALL_NUMBERS[number];
        if (number < 100) {
            int tens = number / 10;
            int units = number % 10;
            return TENS[tens] + (units == 0 ? "" : " " + SMALL_NUMBERS[units]);
        }
        if (number < 1000) {
            int hundreds = number / 100;
            int remainder = number % 100;
            return SMALL_NUMBERS[hundreds] + " hundred"
                    + (remainder == 0 ? "" : " " + numberToEnglish(remainder));
        }
        int thousands = number / 1000;
        int remainder = number % 1000;
        return numberToEnglish(thousands) + " thousand"
                + (remainder == 0 ? "" : " " + numberToEnglish(remainder));
    }

    private static final String[] SMALL_NUMBERS = {
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
            "seventeen", "eighteen", "nineteen"
    };

    private static final String[] TENS = {
            "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"
    };

    @Override
    public void close() {
        synchronized (monitor) {
            closed = true;
            running = false;
            monitor.notifyAll();
        }
        generatorThread.interrupt();
    }
}
