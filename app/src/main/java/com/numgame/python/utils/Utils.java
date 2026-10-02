package com.numgame.python.utils;

import android.content.*;
import android.content.res.*;

public class Utils {
    /** Make this package easy to copy to other apps by avoiding direct "R" references. */
    public static int resId(Context context, String type, String name) {
        Resources resources = context.getResources();
        return resources.getIdentifier(name, type, context.getApplicationInfo().packageName);
    }
}
