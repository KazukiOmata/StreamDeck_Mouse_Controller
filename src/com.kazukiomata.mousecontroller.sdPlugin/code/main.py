import requests
from streamdeck_sdk import (
    StreamDeck,
    Action,
    events_received_objs,
    events_sent_objs,
    image_bytes_to_base64,
    logger,
)

import settings

import pyautogui

class LoremFlickrError(Exception):
    pass


def get_image_from_lorem_flickr(
        category: str,
        union_type: str = "or",
        grayscale_flag: bool = False,
        timeout: float = 5,
) -> str:
    url = settings.LOREM_FLICKR_URL
    if grayscale_flag:
        url += "/g"
    url += f"/{settings.IMAGE_SIZE}/{settings.IMAGE_SIZE}/{category}"
    if union_type == "and":
        url += "/all"
    logger.info(f"{url=}")
    response = requests.get(url, stream=True, timeout=timeout)
    if not response.ok:
        raise LoremFlickrError(f"Bad response. Status code: {response.status_code}")
    image_binary = response.content
    image_mime = response.headers["Content-Type"]
    image_base64 = image_bytes_to_base64(obj=image_binary, image_mime=image_mime)
    return image_base64


class SetKeyImage(Action):
    UUID = "com.kazukiomata.mousecontroller.doubleclick000"

    def on_key_down(self, obj: events_received_objs.KeyDown):
        category = obj.payload.settings.get("category", "kitten")
        union_type = obj.payload.settings.get("union_type", "or")
        grayscale_flag = obj.payload.settings.get("grayscale_flag", False)

        logger.info(f"{category=}, {union_type=}, {grayscale_flag=}")
        try:
            image_base64 = get_image_from_lorem_flickr(
                category=category,
                union_type=union_type,
                grayscale_flag=grayscale_flag,
            )
        except Exception as err:  # noqa
            logger.error(str(err))
            self.show_alert(context=obj.context)
            return

        self.set_image(
            context=obj.context,
            payload=events_sent_objs.SetImagePayload(
                image=image_base64,
                target=0,
                state=obj.payload.state,
            )
        )


class SetDoubleClick(Action):
    UUID = "com.kazukiomata.mousecontroller.doubleclick"

    def on_dial_down(self, obj: events_received_objs.DialDown):
        logger.info("here is dial_down.")
        logger.info(obj)

        _payload = {}

        current_mouse_coordinate_x = pyautogui.position().x
        current_mouse_coordinate_y = pyautogui.position().y

        record_type = obj.payload.settings.get("record_type", "not")

        set_coordinate_x = obj.payload.settings.get("set_coordinate_x", "0")
        set_coordinate_y = obj.payload.settings.get("set_coordinate_y", "0")

        input_coordinate_x = obj.payload.settings.get("input_coordinate_x", "0")
        input_coordinate_y = obj.payload.settings.get("input_coordinate_y", "0")

        set_button = obj.payload.settings.get("set_button", "not")
        logger.info(
            f"{current_mouse_coordinate_x=}, {current_mouse_coordinate_y=}, {set_coordinate_x=}, {set_coordinate_y=}, {input_coordinate_x=}, {input_coordinate_y=}, {set_button=}")
        logger.info(type(set_coordinate_x))
        logger.info("test1")
        logger.info(type(set_coordinate_x))
        logger.info(type(set_coordinate_y))
        # try:
        if (set_button == "clicked") and (record_type == "record-type-input"):
            logger.info("clicked")

            set_coordinate_x = input_coordinate_x
            set_coordinate_y = input_coordinate_y
            logger.info("test2")
        elif (record_type == "record-type-current"):
            logger.info("current")
            set_coordinate_x = current_mouse_coordinate_x
            set_coordinate_y = current_mouse_coordinate_y
        elif (record_type == "record-type-not"):
            logger.info("not record")

        else:
            logger.info("unexpected record-type- : ")
            logger.info(record_type)

        logger.info("test3")
        pyautogui.doubleClick(x=int(set_coordinate_x), y=int(set_coordinate_y))

        logger.info("test5")

        _payload["current_mouse_coordinate_x"] = current_mouse_coordinate_x
        _payload["current_mouse_coordinate_y"] = current_mouse_coordinate_y
        _payload["record_type"] = record_type
        _payload["set_coordinate_x"] = set_coordinate_x
        _payload["set_coordinate_y"] = set_coordinate_y

        _payload["set_button"] = "not"


        self.set_settings(
            context=obj.context,
            payload=_payload
        )





    def on_key_down(self, obj: events_received_objs.KeyDown):

        logger.info("here is key_down.")
        logger.info(obj)

        _payload ={}

        # current_mouse_coordinate_x = obj.payload.settings.get("current_mouse_coordinate_x", "0")
        # current_mouse_coordinate_y = obj.payload.settings.get("current_mouse_coordinate_y", "0")
        current_mouse_coordinate_x = pyautogui.position().x
        current_mouse_coordinate_y = pyautogui.position().y

        record_type = obj.payload.settings.get("record_type", "not")

        set_coordinate_x = obj.payload.settings.get("set_coordinate_x", "0")
        set_coordinate_y = obj.payload.settings.get("set_coordinate_y", "0")

        input_coordinate_x = obj.payload.settings.get("input_coordinate_x", "0")
        input_coordinate_y = obj.payload.settings.get("input_coordinate_y", "0")

        set_button = obj.payload.settings.get("set_button", "not")




        # union_type = obj.payload.settings.get("union_type", "or")
        # grayscale_flag = obj.payload.settings.get("grayscale_flag", False)

        logger.info(f"{current_mouse_coordinate_x=}, {current_mouse_coordinate_y=}, {set_coordinate_x=}, {set_coordinate_y=}, {input_coordinate_x=}, {input_coordinate_y=}, {set_button=}")
        logger.info(type(set_coordinate_x))
        logger.info("test1")
        logger.info(type(set_coordinate_x))
        logger.info(type(set_coordinate_y))
        # try:
        if (set_button == "clicked") and (record_type == "record-type-input"):
            logger.info("clicked")

            set_coordinate_x = input_coordinate_x
            set_coordinate_y = input_coordinate_y
            logger.info("test2")
        elif (record_type == "record-type-current"):
            logger.info("current")
            set_coordinate_x = current_mouse_coordinate_x
            set_coordinate_y = current_mouse_coordinate_y
        elif (record_type == "record-type-not"):
            logger.info("not record")

        else :
            logger.info("unexpected record-type-")
        logger.info("test3")



        # except Exception as err:  # noqa
        #     logger.error(str(err))
        #     # 三角マークを表示
        #     self.show_alert(context=obj.context)
        #     return


        # self.set_image(
        #     context=obj.context,
        #     payload=events_sent_objs.SetImagePayload(
        #         image=image_base64,
        #         target=0,
        #         state=obj.payload.state,
        #     )
        # )
        # double click

        logger.info("test4")



        # pyautogui.rightClick(x=int(set_coordinate_x), y=int(set_coordinate_y))
        pyautogui.doubleClick(x=int(set_coordinate_x), y=int(set_coordinate_y))

        logger.info("test5")

        _payload["current_mouse_coordinate_x"] = current_mouse_coordinate_x
        _payload["current_mouse_coordinate_y"] = current_mouse_coordinate_y
        _payload["record_type"] = record_type
        _payload["set_coordinate_x"] = set_coordinate_x
        _payload["set_coordinate_y"] = set_coordinate_y

        # _payload["input_coordinate_x"] = input_coordinate_x
        # _payload["input_coordinate_y"] = input_coordinate_y
        _payload["set_button"] = "not"


        # self.send_to_property_inspector(
        #     action=self.UUID,
        #     context=obj.context,
        #     payload=_payload
        # )
        self.set_settings(
            context=obj.context,
            payload=_payload
        )






    def on_will_appear(self, obj: events_received_objs.WillAppear):

        logger.info("here is will_appear.")
        logger.info(obj)
        # objはlocalなsettingsが帰ってくる。
        # 2024 - 03 - 19
        # 23: 56:38, 586 - [INFO] - com.kazukiomata.mousecontroller - (main.py).on_will_appear(
        #     171): action = 'com.kazukiomata.mousecontroller.doubleclick'
        # context = 'f474b7676bd12b03ed6489fc94554ee0'
        # device = '23DF7CE1F93859AEB5B11C72ABE2A590'
        # payload = WillAppearPayload(
        #     settings={'current_mouse_coordinate_x': 0, 'current_mouse_coordinate_y': 0, 'input_coordinate_x': '0',
        #               'input_coordinate_y': '0', 'record_type': 'record-type-current', 'set_coordinate_x': 0,
        #               'set_coordinate_y': 0}, coordinates=KeyCoordinates(column=2, row=1), state=None,
        #     isInMultiAction=False, controller= < ControllerEnum.KEYPAD: 'Keypad' >) event = 'willAppear'

        _payload ={}

        _payload = obj.payload.settings
        _payload["event"] = "from on_will_appear"

        self.set_settings(
            context=obj.context,

            payload=_payload
        )


    def on_will_disappear(self, obj: events_received_objs.WillDisappear):

        self.show_alert(context=obj.context)
        logger.info("here is on_will_disappear")
        logger.info(obj)


        # _global_payload = {}
        # _global_payload["event"] = "will_disappear"
        # _global_payload["test"] = 1

        # globalはpayloadだけでよい
        # self.set_global_settings(
        #     payload=_global_payload
        # )



    # self.send_to_property_inspector(
        #     action=self.UUID,
        #     context=obj.context,
        #     payload=_payload
        # )

class SetClick(Action):
    UUID = "com.kazukiomata.mousecontroller.click"

    def on_dial_down(self, obj: events_received_objs.DialDown):
        logger.info("here is dial_down.")
        logger.info(obj)

        _payload = {}

        current_mouse_coordinate_x = pyautogui.position().x
        current_mouse_coordinate_y = pyautogui.position().y

        record_type = obj.payload.settings.get("record_type", "not")

        set_coordinate_x = obj.payload.settings.get("set_coordinate_x", "0")
        set_coordinate_y = obj.payload.settings.get("set_coordinate_y", "0")

        input_coordinate_x = obj.payload.settings.get("input_coordinate_x", "0")
        input_coordinate_y = obj.payload.settings.get("input_coordinate_y", "0")

        set_button = obj.payload.settings.get("set_button", "not")
        logger.info(
            f"{current_mouse_coordinate_x=}, {current_mouse_coordinate_y=}, {set_coordinate_x=}, {set_coordinate_y=}, {input_coordinate_x=}, {input_coordinate_y=}, {set_button=}")
        logger.info(type(set_coordinate_x))
        logger.info("test1")
        logger.info(type(set_coordinate_x))
        logger.info(type(set_coordinate_y))
        # try:
        if (set_button == "clicked") and (record_type == "record-type-input"):
            logger.info("clicked")

            set_coordinate_x = input_coordinate_x
            set_coordinate_y = input_coordinate_y
            logger.info("test2")
        elif (record_type == "record-type-current"):
            logger.info("current")
            set_coordinate_x = current_mouse_coordinate_x
            set_coordinate_y = current_mouse_coordinate_y
        elif (record_type == "record-type-not"):
            logger.info("not record")

        else:
            logger.info("unexpected record-type- : ")
            logger.info(record_type)

        logger.info("test3")
        pyautogui.doubleClick(x=int(set_coordinate_x), y=int(set_coordinate_y))

        logger.info("test5")

        _payload["current_mouse_coordinate_x"] = current_mouse_coordinate_x
        _payload["current_mouse_coordinate_y"] = current_mouse_coordinate_y
        _payload["record_type"] = record_type
        _payload["set_coordinate_x"] = set_coordinate_x
        _payload["set_coordinate_y"] = set_coordinate_y

        _payload["set_button"] = "not"


        self.set_settings(
            context=obj.context,
            payload=_payload
        )





    def on_key_down(self, obj: events_received_objs.KeyDown):

        logger.info("here is key_down.")
        logger.info(obj)

        _payload ={}

        # current_mouse_coordinate_x = obj.payload.settings.get("current_mouse_coordinate_x", "0")
        # current_mouse_coordinate_y = obj.payload.settings.get("current_mouse_coordinate_y", "0")
        current_mouse_coordinate_x = pyautogui.position().x
        current_mouse_coordinate_y = pyautogui.position().y

        record_type = obj.payload.settings.get("record_type", "not")

        set_coordinate_x = obj.payload.settings.get("set_coordinate_x", "0")
        set_coordinate_y = obj.payload.settings.get("set_coordinate_y", "0")

        input_coordinate_x = obj.payload.settings.get("input_coordinate_x", "0")
        input_coordinate_y = obj.payload.settings.get("input_coordinate_y", "0")

        set_button = obj.payload.settings.get("set_button", "not")




        # union_type = obj.payload.settings.get("union_type", "or")
        # grayscale_flag = obj.payload.settings.get("grayscale_flag", False)

        logger.info(f"{current_mouse_coordinate_x=}, {current_mouse_coordinate_y=}, {set_coordinate_x=}, {set_coordinate_y=}, {input_coordinate_x=}, {input_coordinate_y=}, {set_button=}")
        logger.info(type(set_coordinate_x))
        logger.info("test1")
        logger.info(type(set_coordinate_x))
        logger.info(type(set_coordinate_y))
        # try:
        if (set_button == "clicked") and (record_type == "record-type-input"):
            logger.info("clicked")

            set_coordinate_x = input_coordinate_x
            set_coordinate_y = input_coordinate_y
            logger.info("test2")
        elif (record_type == "record-type-current"):
            logger.info("current")
            set_coordinate_x = current_mouse_coordinate_x
            set_coordinate_y = current_mouse_coordinate_y
        elif (record_type == "record-type-not"):
            logger.info("not record")

        else :
            logger.info("unexpected record-type-")
        logger.info("test3")



        # except Exception as err:  # noqa
        #     logger.error(str(err))
        #     # 三角マークを表示
        #     self.show_alert(context=obj.context)
        #     return


        # self.set_image(
        #     context=obj.context,
        #     payload=events_sent_objs.SetImagePayload(
        #         image=image_base64,
        #         target=0,
        #         state=obj.payload.state,
        #     )
        # )
        # double click

        logger.info("test4")



        # pyautogui.rightClick(x=int(set_coordinate_x), y=int(set_coordinate_y))
        pyautogui.click(x=int(set_coordinate_x), y=int(set_coordinate_y))

        logger.info("test5")

        _payload["current_mouse_coordinate_x"] = current_mouse_coordinate_x
        _payload["current_mouse_coordinate_y"] = current_mouse_coordinate_y
        _payload["record_type"] = record_type
        _payload["set_coordinate_x"] = set_coordinate_x
        _payload["set_coordinate_y"] = set_coordinate_y

        # _payload["input_coordinate_x"] = input_coordinate_x
        # _payload["input_coordinate_y"] = input_coordinate_y
        _payload["set_button"] = "not"


        # self.send_to_property_inspector(
        #     action=self.UUID,
        #     context=obj.context,
        #     payload=_payload
        # )
        self.set_settings(
            context=obj.context,
            payload=_payload
        )






    def on_will_appear(self, obj: events_received_objs.WillAppear):

        logger.info("here is will_appear.")
        logger.info(obj)
        # objはlocalなsettingsが帰ってくる。
        # 2024 - 03 - 19
        # 23: 56:38, 586 - [INFO] - com.kazukiomata.mousecontroller - (main.py).on_will_appear(
        #     171): action = 'com.kazukiomata.mousecontroller.doubleclick'
        # context = 'f474b7676bd12b03ed6489fc94554ee0'
        # device = '23DF7CE1F93859AEB5B11C72ABE2A590'
        # payload = WillAppearPayload(
        #     settings={'current_mouse_coordinate_x': 0, 'current_mouse_coordinate_y': 0, 'input_coordinate_x': '0',
        #               'input_coordinate_y': '0', 'record_type': 'record-type-current', 'set_coordinate_x': 0,
        #               'set_coordinate_y': 0}, coordinates=KeyCoordinates(column=2, row=1), state=None,
        #     isInMultiAction=False, controller= < ControllerEnum.KEYPAD: 'Keypad' >) event = 'willAppear'

        _payload ={}

        _payload = obj.payload.settings
        _payload["event"] = "from on_will_appear"

        self.set_settings(
            context=obj.context,

            payload=_payload
        )


    def on_will_disappear(self, obj: events_received_objs.WillDisappear):

        self.show_alert(context=obj.context)
        logger.info("here is on_will_disappear")
        logger.info(obj)


        # _global_payload = {}
        # _global_payload["event"] = "will_disappear"
        # _global_payload["test"] = 1

        # globalはpayloadだけでよい
        # self.set_global_settings(
        #     payload=_global_payload
        # )



    # self.send_to_property_inspector(
        #     action=self.UUID,
        #     context=obj.context,
        #     payload=_payload
        # )



class SetRightClick(Action):
    UUID = "com.kazukiomata.mousecontroller.rightclick"

    def on_dial_down(self, obj: events_received_objs.DialDown):
        logger.info("here is dial_down.")
        logger.info(obj)

        _payload = {}

        current_mouse_coordinate_x = pyautogui.position().x
        current_mouse_coordinate_y = pyautogui.position().y

        record_type = obj.payload.settings.get("record_type", "not")

        set_coordinate_x = obj.payload.settings.get("set_coordinate_x", "0")
        set_coordinate_y = obj.payload.settings.get("set_coordinate_y", "0")

        input_coordinate_x = obj.payload.settings.get("input_coordinate_x", "0")
        input_coordinate_y = obj.payload.settings.get("input_coordinate_y", "0")

        set_button = obj.payload.settings.get("set_button", "not")
        logger.info(
            f"{current_mouse_coordinate_x=}, {current_mouse_coordinate_y=}, {set_coordinate_x=}, {set_coordinate_y=}, {input_coordinate_x=}, {input_coordinate_y=}, {set_button=}")
        logger.info(type(set_coordinate_x))
        logger.info("test1")
        logger.info(type(set_coordinate_x))
        logger.info(type(set_coordinate_y))
        # try:
        if (set_button == "clicked") and (record_type == "record-type-input"):
            logger.info("clicked")

            set_coordinate_x = input_coordinate_x
            set_coordinate_y = input_coordinate_y
            logger.info("test2")
        elif (record_type == "record-type-current"):
            logger.info("current")
            set_coordinate_x = current_mouse_coordinate_x
            set_coordinate_y = current_mouse_coordinate_y
        elif (record_type == "record-type-not"):
            logger.info("not record")

        else:
            logger.info("unexpected record-type- : ")
            logger.info(record_type)

        logger.info("test3")
        pyautogui.click(int(set_coordinate_x), int(set_coordinate_y), 2, 0.1, 'left')  # ダブルクリック
        # pyautogui.doubleClick(x=int(set_coordinate_x), y=int(set_coordinate_y))

        logger.info("test5")

        _payload["current_mouse_coordinate_x"] = current_mouse_coordinate_x
        _payload["current_mouse_coordinate_y"] = current_mouse_coordinate_y
        _payload["record_type"] = record_type
        _payload["set_coordinate_x"] = set_coordinate_x
        _payload["set_coordinate_y"] = set_coordinate_y

        _payload["set_button"] = "not"


        self.set_settings(
            context=obj.context,
            payload=_payload
        )





    def on_key_down(self, obj: events_received_objs.KeyDown):

        logger.info("here is key_down.")
        logger.info(obj)

        _payload ={}

        # current_mouse_coordinate_x = obj.payload.settings.get("current_mouse_coordinate_x", "0")
        # current_mouse_coordinate_y = obj.payload.settings.get("current_mouse_coordinate_y", "0")
        current_mouse_coordinate_x = pyautogui.position().x
        current_mouse_coordinate_y = pyautogui.position().y

        record_type = obj.payload.settings.get("record_type", "not")

        set_coordinate_x = obj.payload.settings.get("set_coordinate_x", "0")
        set_coordinate_y = obj.payload.settings.get("set_coordinate_y", "0")

        input_coordinate_x = obj.payload.settings.get("input_coordinate_x", "0")
        input_coordinate_y = obj.payload.settings.get("input_coordinate_y", "0")

        set_button = obj.payload.settings.get("set_button", "not")




        # union_type = obj.payload.settings.get("union_type", "or")
        # grayscale_flag = obj.payload.settings.get("grayscale_flag", False)

        logger.info(f"{current_mouse_coordinate_x=}, {current_mouse_coordinate_y=}, {set_coordinate_x=}, {set_coordinate_y=}, {input_coordinate_x=}, {input_coordinate_y=}, {set_button=}")
        logger.info(type(set_coordinate_x))
        logger.info("test1")
        logger.info(type(set_coordinate_x))
        logger.info(type(set_coordinate_y))
        # try:
        if (set_button == "clicked") and (record_type == "record-type-input"):
            logger.info("clicked")

            set_coordinate_x = input_coordinate_x
            set_coordinate_y = input_coordinate_y
            logger.info("test2")
        elif (record_type == "record-type-current"):
            logger.info("current")
            set_coordinate_x = current_mouse_coordinate_x
            set_coordinate_y = current_mouse_coordinate_y
        elif (record_type == "record-type-not"):
            logger.info("not record")

        else :
            logger.info("unexpected record-type-")
        logger.info("test3")



        # except Exception as err:  # noqa
        #     logger.error(str(err))
        #     # 三角マークを表示
        #     self.show_alert(context=obj.context)
        #     return


        # self.set_image(
        #     context=obj.context,
        #     payload=events_sent_objs.SetImagePayload(
        #         image=image_base64,
        #         target=0,
        #         state=obj.payload.state,
        #     )
        # )
        # double click

        logger.info("test4")



        # pyautogui.rightClick(x=int(set_coordinate_x), y=int(set_coordinate_y))
        pyautogui.rightClick(x=int(set_coordinate_x), y=int(set_coordinate_y))

        logger.info("test5")

        _payload["current_mouse_coordinate_x"] = current_mouse_coordinate_x
        _payload["current_mouse_coordinate_y"] = current_mouse_coordinate_y
        _payload["record_type"] = record_type
        _payload["set_coordinate_x"] = set_coordinate_x
        _payload["set_coordinate_y"] = set_coordinate_y

        # _payload["input_coordinate_x"] = input_coordinate_x
        # _payload["input_coordinate_y"] = input_coordinate_y
        _payload["set_button"] = "not"


        # self.send_to_property_inspector(
        #     action=self.UUID,
        #     context=obj.context,
        #     payload=_payload
        # )
        self.set_settings(
            context=obj.context,
            payload=_payload
        )






    def on_will_appear(self, obj: events_received_objs.WillAppear):

        logger.info("here is will_appear.")
        logger.info(obj)
        # objはlocalなsettingsが帰ってくる。
        # 2024 - 03 - 19
        # 23: 56:38, 586 - [INFO] - com.kazukiomata.mousecontroller - (main.py).on_will_appear(
        #     171): action = 'com.kazukiomata.mousecontroller.doubleclick'
        # context = 'f474b7676bd12b03ed6489fc94554ee0'
        # device = '23DF7CE1F93859AEB5B11C72ABE2A590'
        # payload = WillAppearPayload(
        #     settings={'current_mouse_coordinate_x': 0, 'current_mouse_coordinate_y': 0, 'input_coordinate_x': '0',
        #               'input_coordinate_y': '0', 'record_type': 'record-type-current', 'set_coordinate_x': 0,
        #               'set_coordinate_y': 0}, coordinates=KeyCoordinates(column=2, row=1), state=None,
        #     isInMultiAction=False, controller= < ControllerEnum.KEYPAD: 'Keypad' >) event = 'willAppear'

        _payload ={}

        _payload = obj.payload.settings
        _payload["event"] = "from on_will_appear"

        self.set_settings(
            context=obj.context,

            payload=_payload
        )


    def on_will_disappear(self, obj: events_received_objs.WillDisappear):

        self.show_alert(context=obj.context)
        logger.info("here is on_will_disappear")
        logger.info(obj)


        # _global_payload = {}
        # _global_payload["event"] = "will_disappear"
        # _global_payload["test"] = 1

        # globalはpayloadだけでよい
        # self.set_global_settings(
        #     payload=_global_payload
        # )



    # self.send_to_property_inspector(
        #     action=self.UUID,
        #     context=obj.context,
        #     payload=_payload
        # )





if __name__ == '__main__':
    StreamDeck(
        actions=[
            SetDoubleClick(),
            SetClick(),
            SetRightClick(),
        ],
        log_file=settings.LOG_FILE_PATH,
        log_level=settings.LOG_LEVEL,
        log_backup_count=1,
    ).run()


# $PI.getSettings(action, jsn =>{
#         console.log("")
#         console.log('Property Inspector connected', jsn);
#         console.log("jsn.actionInfo.payload.settings : ");
#         console.log(jsn.actionInfo.payload.settings);
#
#         settings = jsn.actionInfo.payload.settings;
#
#         if (settings?.current_mouse_coordinate_x) {
#             current_mouse_coordinate_x_el.value = settings.current_mouse_coordinate_x
#         } else {
#             current_mouse_coordinate_x_el.value = 0
#             settings["current_mouse_coordinate_x"] = current_mouse_coordinate_x_el.value
#         }
#         if (settings?.current_mouse_coordinate_y) {
#             current_mouse_coordinate_y_el.value = settings.current_mouse_coordinate_y
#         } else {
#             current_mouse_coordinate_y_el.value = 0
#             settings["current_mouse_coordinate_y"] = current_mouse_coordinate_y_el.value
#         }
#     });