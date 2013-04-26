import sublime_plugin
import sublime

class CSSSelectorReveal(sublime_plugin.EventListener):

    def on_selection_modified(self, view):
        latest_close_brace = None

        # See if the user has selected the end of a CSS rule
        for region in view.sel():
            if view.substr(region) == '}':
                latest_close_brace = region

        # Look for a matching opening brace and show a status.
        if latest_close_brace != None:
            matching_open = self.find_matching_open_brace(view, latest_close_brace)
            if (matching_open != None):
                # The numeric prefix puts us on the far left of the status bar
                view.set_status('1css_selector', "CSS: " + matching_open)
                return

        # Keep usage clean: clear the status if we have no direct match
        view.erase_status('1css_selector')


    def find_matching_open_brace(self, view, close_brace_region):
        openers_required = 1
        search_backwards_from = close_brace_region.begin()

        while search_backwards_from > 0:
            next_search = sublime.Region(search_backwards_from - 1, search_backwards_from)
            haystack = view.substr(next_search)

            # Look for an exactly matching opening brace, fail in all other cases.
            if haystack == '{':
                openers_required -= 1

            elif haystack == '}':
                openers_required += 1

            # If we've found an opening brace, extract the text before the brace from that line
            if openers_required == 0:
                return self.selector_text(view, next_search.begin())

            search_backwards_from -= 1

        return None

    def selector_text(self, view, opening_brace_position):
        line_with_selector = view.line(sublime.Region(opening_brace_position, opening_brace_position))

        selector = 'redacted'
        if line_with_selector != None:
            line_text = view.substr(line_with_selector).strip(" \t\n\r{")

            if len(line_text) == 0:
                return "<TODO: previous line>"
            else:
                return line_text

        return selector
