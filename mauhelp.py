from maubot import Plugin, MessageEvent
from maubot.handlers import command
from mautrix.types import EventType


class MauHelp(Plugin):
    @command.new(name="help", help="Shows this help text")
    async def help(self, evt: MessageEvent):
        help_text_dict = {}
        for handler_func in self.client.event_handlers[EventType.ROOM_MESSAGE]:
            command_help = ""
            if hasattr(handler_func, "__mb_name__") and hasattr(handler_func, "__mb_usage_inline__"):
                # Initialize the key if it doesn't exist
                if handler_func.__mb_name__ not in help_text_dict:
                    help_text_dict[handler_func.__mb_name__] = ""

                if handler_func.__mb_help__ is not None:
                    command_help = f" - {handler_func.__mb_help__}"
                help_text_dict[handler_func.__mb_name__] += f"{handler_func.__mb_usage_without_subcommands__}{command_help}\n"

                if not handler_func.__mb_require_subcommand__:
                    help_text_dict[handler_func.__mb_name__] += f"* {handler_func.__mb_prefix__} {handler_func.__mb_usage_args__} - {handler_func.__mb_help__}\n"

                help_text_dict[handler_func.__mb_name__] += "\n".join(cmd.__mb_usage_inline__ for cmd in handler_func.__mb_subcommands__) + "\n"

        help_text = ""
        for plugin in help_text_dict:
            help_text += f"\n{help_text_dict[plugin]}\n"

        await evt.reply(help_text)
