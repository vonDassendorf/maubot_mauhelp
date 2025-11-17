from maubot import Plugin, MessageEvent
from maubot.handlers import command
from mautrix.types import EventType


class MauHelp(Plugin):
    @command.new(name="help", help="Shows this help text")
    async def help(self, evt: MessageEvent):
        help_text_dict = {}
        for command_handler in self.client.event_handlers[EventType.ROOM_MESSAGE]:
            if hasattr(command_handler, '__mb_name__') and hasattr(command_handler, '__mb_usage_inline__'):
                cmd = command_handler.__mb_name__
                if not cmd in help_text_dict:
                    help_text_dict[cmd] = ""

                help_text_dict[cmd] += command_handler.__mb_usage_without_subcommands__ + "\n"
                if command_handler.__mb_help__:
                    help_text_dict[cmd] += f"-> {command_handler.__mb_help__}\n"
                    
                if not command_handler.__mb_require_subcommand__:
                    help_text_dict[cmd] += f"* {command_handler.__mb_prefix__} {command_handler.__mb_usage_args__} - {command_handler.__mb_help__}\n"
                
                help_text_dict[cmd] += "\n".join(cmd.__mb_usage_inline__ for cmd in command_handler.__mb_subcommands__)+"\n"
                
        help_text = ''
        for plugin in help_text_dict:
            help_text += f"\n{help_text_dict[plugin]}\n"

        await evt.reply(help_text)
