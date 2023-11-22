#include "djui.h"

static struct DjuiTheme sDjuiThemeLight = {
    .id = "LIGHT_THEME",
    .name = "LIGHT_THEME",
    .interactables = {
        .textColor = {
            11, 11, 11, 255
        },

        .defaultRectColor = {
            222, 222, 222, 255
        },
        .cursorDownRectColor = {
            204, 228, 247, 255
        },
        .hoveredRectColor = {
            229, 241, 251, 255
        },

        .defaultBorderColor = {
            75, 75, 75, 255
        },
        .cursorDownBorderColor = {
            0, 84, 153, 255
        },
        .hoveredBorderColor = {
            0, 120, 215, 255
        }
    },
    .threePanels = {
        .rectColor = {
            0, 0, 0, 235
        },
        .borderColor = {
            0, 0, 0, 200
        }
    },
    .panels = {
        .hudFontHeader = false
    }
};

static struct DjuiTheme sDjuiThemeDark = {
    .id = "DARK_THEME",
    .name = "DARK_THEME",
    .interactables = {
        .textColor = {
            220, 220, 220, 255
        },

        .defaultRectColor = {
            22, 22, 22, 255
        },
        .cursorDownRectColor = {
            100, 100, 100, 255
        },
        .hoveredRectColor = {
            80, 80, 80, 255
        },

        .defaultBorderColor = {
            75, 75, 75, 255
        },
        .cursorDownBorderColor = {
            0, 84, 153, 255
        },
        .hoveredBorderColor = {
            0, 120, 215, 255
        }
    },
    .threePanels = {
        .rectColor = {
            0, 0, 0, 235
        },
        .borderColor = {
            0, 0, 0, 200
        }
    },
    .panels = {
        .hudFontHeader = false
    }
};

static struct DjuiTheme sDjuiThemeFileSelect = {
    .id = "FILE_SELECT_THEME",
    .name = "FILE_SELECT_THEME",
    .interactables = {
        .textColor = {
            11, 11, 11, 255
        },

        .defaultRectColor = {
            200, 215, 197, 255
        },
        .cursorDownRectColor = {
            204, 228, 247, 255
        },
        .hoveredRectColor = {
            229, 241, 251, 255
        },

        .defaultBorderColor = {
            74, 79, 74, 255
        },
        .cursorDownBorderColor = {
            0, 84, 153, 255
        },
        .hoveredBorderColor = {
            0, 120, 215, 255
        }
    },
    .threePanels = {
        .rectColor = {
            208, 165, 32, 255
        },
        .borderColor = {
            182, 135, 8, 255
        }
    },
    .panels = {
        .hudFontHeader = true
    }
};

static struct DjuiTheme sDjuiThemeMario = {
    .id = "MARIO_THEME",
    .name = "MARIO_THEME",
    .interactables = {
        .textColor = {
            11, 11, 11, 255
        },

        .defaultRectColor = {
            255, 227, 0, 255
        },
        .cursorDownRectColor = {
            204, 228, 247, 255
        },
        .hoveredRectColor = {
            229, 241, 251, 255
        },

        .defaultBorderColor = {
            196, 165, 0, 255
        },
        .cursorDownBorderColor = {
            0, 84, 153, 255
        },
        .hoveredBorderColor = {
            0, 120, 215, 255
        }
    },
    .threePanels = {
        .rectColor = {
            76, 116, 201, 235
        },
        .borderColor = {
            255, 82, 82, 200
        }
    },
    .panels = {
        .hudFontHeader = false
    }
};

struct DjuiTheme* gDjuiThemes[] = {
    &sDjuiThemeLight,
    &sDjuiThemeDark,
    &sDjuiThemeFileSelect,
    &sDjuiThemeMario
};

struct DjuiColor djui_theme_shade_color(struct DjuiColor color) {
    color.r *= 0.75f;
    color.g *= 0.75f;
    color.b *= 0.75f;
    return color;
}

void djui_themes_init(void) {
    for (s32 i = 0; i < DJUI_THEME_MAX; i++) {
        gDjuiThemes[i]->name = djui_language_get("DJUI_THEMES", gDjuiThemes[i]->id);
    }
}
