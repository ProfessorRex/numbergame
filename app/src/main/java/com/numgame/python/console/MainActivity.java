package com.numgame.python.console;

import android.app.*;
import com.numgame.python.utils.*;
import com.numgame.python.utils.PythonConsoleActivity;

public class MainActivity extends PythonConsoleActivity {

    @Override protected Class<? extends Task> getTaskClass() {
        return Task.class;
    }

    public static class Task extends PythonConsoleActivity.Task {
        public Task(Application app) {
            super(app);
        }

        @Override public void run() {
            py.getModule("numgame").callAttr("main");
        }
    }
}
