package com.numgame.python.console;

import org.junit.Test;

import java.lang.reflect.Field;
import java.util.ArrayDeque;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class NumberGameEngineTest {
    @Test
    public void hintIsSeededAndLimitedToOnePerQuestion() throws Exception {
        NumberGameEngine firstGame = new NumberGameEngine();
        NumberGameEngine secondGame = new NumberGameEngine();
        try {
            NumberGameEngine.Question firstQuestion = start(firstGame, 118999L);
            NumberGameEngine.Question secondQuestion = start(secondGame, 118999L);
            assertEquals(clueTexts(firstQuestion), clueTexts(secondQuestion));
            assertEquals(3, firstGame.getHintsAvailable());

            NumberGameEngine.HintResult firstHint = firstGame.requestHint();
            NumberGameEngine.HintResult secondHint = secondGame.requestHint();
            assertFalse(firstHint.unavailable);
            assertFalse(firstHint.alreadyUsed);
            assertEquals(firstHint.question.clues.get(3).text,
                    secondHint.question.clues.get(3).text);
            assertEquals(4, firstHint.question.clues.size());
            assertTrue(firstHint.question.solutionCount <= firstQuestion.solutionCount);
            assertEquals(2, firstGame.getHintsAvailable());

            NumberGameEngine.HintResult repeatedHint = firstGame.requestHint();
            assertTrue(repeatedHint.alreadyUsed);
            assertEquals(2, firstGame.getHintsAvailable());
        } finally {
            firstGame.close();
            secondGame.close();
        }
    }

    @Test
    public void levelsAdvanceEveryEightCorrectAnswersAndQueueUsesFutureLevels()
            throws Exception {
        NumberGameEngine engine = new NumberGameEngine();
        try {
            NumberGameEngine.Question question = start(engine, 118999L);
            awaitQueueSize(engine, 8);
            Field queuedQuestions = NumberGameEngine.GameSnapshot.class
                    .getDeclaredField("futureQuestions");
            queuedQuestions.setAccessible(true);
            @SuppressWarnings("unchecked")
            ArrayDeque<NumberGameEngine.Question> queue = (ArrayDeque<NumberGameEngine.Question>)
                    queuedQuestions.get(engine.createSnapshot());
            int index = 0;
            for (NumberGameEngine.Question queued : queue) {
                assertEquals(index < 7 ? 1 : 2, queued.level);
                index++;
            }

            for (int answered = 1; answered <= 8; answered++) {
                NumberGameEngine.AnswerResult result = engine.submitAnswer(
                        Integer.toString(firstSolution(question)));
                assertEquals(NumberGameEngine.AnswerStatus.CORRECT, result.status);
                assertEquals(answered == 8, result.levelUp);
                if (answered < 8) {
                    question = nextQuestion(engine);
                    assertEquals(1, question.level);
                }
            }

            assertEquals(2, engine.getLevel());
            assertEquals(1, engine.getLevelUpEvents().size());
            NumberGameEngine.LevelUpEvent levelUp = engine.getLevelUpEvents().get(0);
            assertEquals(2, levelUp.level);
            assertTrue(levelUp.timestampMillis > 0);

            NumberGameEngine restored = new NumberGameEngine();
            try {
                restored.restoreGame(engine.createSnapshot(), ignored -> { });
                assertEquals(1, restored.getLevelUpEvents().size());
                assertEquals(levelUp.timestampMillis,
                        restored.getLevelUpEvents().get(0).timestampMillis);
            } finally {
                restored.close();
            }
            assertEquals(2, nextQuestion(engine).level);
        } finally {
            engine.close();
        }
    }

    private NumberGameEngine.Question start(NumberGameEngine engine, long seed)
            throws InterruptedException {
        CountDownLatch ready = new CountDownLatch(1);
        AtomicReference<NumberGameEngine.Question> question = new AtomicReference<>();
        engine.startGame(1, seed, value -> {
            question.set(value);
            ready.countDown();
        });
        assertTrue("question generation timed out", ready.await(5, TimeUnit.SECONDS));
        return question.get();
    }

    private String clueTexts(NumberGameEngine.Question question) {
        StringBuilder result = new StringBuilder();
        for (NumberGameEngine.Clue clue : question.clues) {
            result.append(clue.text).append('\n');
        }
        return result.toString();
    }

    private int firstSolution(NumberGameEngine.Question question) throws Exception {
        Field solutions = NumberGameEngine.Question.class.getDeclaredField("solutions");
        solutions.setAccessible(true);
        return ((java.util.List<Integer>) solutions.get(question)).get(0);
    }

    private NumberGameEngine.Question nextQuestion(NumberGameEngine engine)
            throws InterruptedException {
        CountDownLatch ready = new CountDownLatch(1);
        AtomicReference<NumberGameEngine.Question> question = new AtomicReference<>();
        engine.requestNextQuestion(value -> {
            question.set(value);
            ready.countDown();
        });
        assertTrue("next question generation timed out", ready.await(5, TimeUnit.SECONDS));
        return question.get();
    }

    private void awaitQueueSize(NumberGameEngine engine, int minimumSize)
            throws InterruptedException {
        long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(5);
        while (engine.getQueuedQuestionCount() < minimumSize && System.nanoTime() < deadline) {
            Thread.yield();
        }
        assertTrue("future question queue did not fill", engine.getQueuedQuestionCount() >= minimumSize);
    }
}