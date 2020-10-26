from typing import Set, Optional, Dict, Type

from ..core.help import MainUsageFormatter, format_stage_usage
from ..core.plugin import (
    get_all_plugins_by_type,
    get_all_plugin_names,
    get_all_domains,
    try_translate_domains
)
from ..core.specifier import *
from ..core.specifier.util import specifier_type_string
from ._MainSettings import MainSettings


def format_help() -> str:
    """
    Formats the -h/--help message for wai.annotations.

    :return:    The help message.
    """
    return MainSettings.get_configured_parser(
        prog="convert-annotations",
        formatter_class=MainUsageFormatter
        ).format_help() +\
           ("\n"
            "See following URLs for usage and examples:\n" +
            "https://github.com/waikato-ufdl/wai-annotations/blob/master/doc/USAGE.md\n" +
            "https://github.com/waikato-ufdl/wai-annotations/blob/master/doc/EXAMPLES.md\n")


def list_plugins() -> str:
    """
    Creates a string listing the names of all plugins registered
    with wai.annotations.

    :return:    The formatted string.
    """
    # Get a list of all plugin names
    plugin_names = list(get_all_plugin_names())

    # Sort it alphabetically
    plugin_names.sort()

    return "PLUGINS:\n  " + "\n  ".join(plugin_names) + "\n"


def list_domains() -> str:
    """
    Creates a string listing the names of all domains registered
    with wai.annotations.

    :return:    The formatted string.
    """
    # Get a list of all plugin names
    domain_names = list(domain.name() for domain in get_all_domains())

    # Sort it alphabetically
    domain_names.sort()

    return "DOMAINS:\n  " + "\n  ".join(domain_names) + "\n"


def help_plugins(plugins: Optional[Set[str]] = None) -> str:
    """
    Creates a string listing the plugins registered with wai-annotations,
    including details on their usage.

    :param plugins:     An optional set of plugin names to filter down to.
                        If None, all plugins are displayed.
    :return:            The formatted string.
    """
    # Get the plugins, grouped by type
    all_plugins_by_type = get_all_plugins_by_type()

    # If specific names are provided, filter
    if plugins is not None:
        filter_plugins(all_plugins_by_type, plugins)

    # Header
    result = "PLUGINS:\n"

    # If all plugins are filtered out, display None
    if len(all_plugins_by_type) == 0:
        result += "  NONE\n"

    for base_type, plugins_for_type in all_plugins_by_type.items():
        base_type_string = specifier_type_string(base_type)
        result += f"  {base_type_string.upper()}:\n"
        for name, plugin in plugins_for_type.items():
            result += f"    {name.upper()}:\n"
            result += f"      {plugin.description()}\n\n"
            result += f"      Domain(s): {plugin_domains(plugin)}\n\n"
            result += f"{format_stage_usage(plugin, name, 6)}\n"

        # Additional separation between categories of plugins
        result += "\n"

    return result


def plugin_domains(plugin: Type[StageSpecifier]) -> str:
    """
    Formats a string listing the domains valid for a given plugin.

    :param plugin:  The plugin specifier.
    :return:        The formatted list of domains.
    """
    if issubclass(plugin, SourceStageSpecifier):
        return plugin.domain().name()
    elif issubclass(plugin, SinkStageSpecifier):
        return plugin.domain().name()
    elif issubclass(plugin, ProcessorStageSpecifier):
        return ", ".join(
            domain.name()
            for domain in try_translate_domains(plugin, get_all_domains())
        )


def filter_plugins(plugins_by_type: Dict[Type[StageSpecifier], Dict[str, Type[StageSpecifier]]], filter_set: Set[str]):
    """
    Filters the plugins in place based on their presence in the given set.

    :param plugins_by_type:     The plugins, grouped by type.
    :param filter_set:          The set of plugin names to filter down to.
    """
    # Get the current set of plugin types
    plugin_types = set(plugins_by_type.keys())

    # Process each plugin type separately
    for plugin_type in plugin_types:
        # Get the names of all plugins of this type
        plugin_names = set(plugins_by_type[plugin_type].keys())

        # Remove those names that are not in the filter set
        for plugin_name in plugin_names:
            if plugin_name not in filter_set:
                del plugins_by_type[plugin_type][plugin_name]

        # If all plugins of this type were removed, remove the type as well
        if len(plugins_by_type[plugin_type]) == 0:
            del plugins_by_type[plugin_type]
