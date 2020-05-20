from module.base.timer import Timer
from module.combat.combat import Combat
from module.handler.assets import *
from module.logger import logger
from datetime import datetime, timedelta
from module.ui.ui import MAIN_CHECK, EVENT_LIST_CHECK, BACK_ARROW


class LoginHandler(Combat):
    start_time = datetime.now()

    def handle_app_login(self):
        logger.hr('App login')

        confirm_timer = Timer(1.5, count=4)
        while 1:
            self.device.screenshot()

            if self.handle_get_items(save_get_items=False):
                continue
            if self.handle_get_ship():
                continue
            if self.appear_then_click(LOGIN_ANNOUNCE, offset=(30, 30), interval=1):
                continue
            if self.appear(EVENT_LIST_CHECK, offset=(30, 30), interval=1):
                self.device.click(BACK_ARROW)
                continue
            if self.appear_then_click(LOGIN_GAME_UPDATE, offset=(30, 30), interval=1):
                continue
            if self.appear_then_click(LOGIN_RETURN_SIGN, offset=(30, 30), interval=1):
                continue

            if self.info_bar_count() and self.appear_then_click(LOGIN_CHECK, interval=0.5):
                logger.info('Login success')
            if self.appear(MAIN_CHECK):
                if confirm_timer.reached():
                    logger.info('Login to main confirm')
                    break
            else:
                confirm_timer.reset()

        return True

    def app_restart(self):
        logger.hr('App restart')
        self.device.app_stop()
        self.device.app_start()
        self.handle_app_login()

    def app_ensure_start(self):
        if not self.device.app_is_running():
            self.device.app_start()
            self.handle_app_login()
            return True

        return False

    def _triggered_app_restart(self):
        """
        Returns:
            bool: If triggered a restart condition.
        """
        now = datetime.now()
        if now.date() != self.start_time.date():
            logger.hr('Triggered restart new day')
            return True
        if not self.config.IGNORE_LOW_EMOTION_WARN:
            # The game does not calculate emotion correctly, which is a bug in AzurLane.
            # After a long run, we have to restart the game to update it.
            if now - self.start_time > timedelta(hours=2):
                logger.hr('Triggered restart avoid emotion bug')
                return True

        return False

    def handle_app_restart(self):
        if self._triggered_app_restart():
            self.app_restart()
            self.start_time = datetime.now()
            return True

        return False
