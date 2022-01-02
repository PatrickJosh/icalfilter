# Copyright (C) 2021  Joshua Noeske
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import icalendar
import http.server
import configparser
import urllib.request
import re

conf = configparser.RawConfigParser()
conf.read("./icalfilter.conf")
original_url = conf.get("icalfilter", "original_url")
token = conf.get("icalfilter", "token")
summary_regex_string = conf.get("icalfilter", "summary_regex")
summary_regex = re.compile(summary_regex_string)


def filter_ical():
    original_ical = urllib.request.urlopen(original_url)
    cal = icalendar.Calendar.from_ical(original_ical.read())
    new_cal = icalendar.Calendar()

    # To include attributes before first event.
    for k, v in cal.items():
        new_cal.add(k, v)

    # Go through all events and add all events whose summary does not match the given regex to the new calendar
    for element in cal.walk():
        if element.name == "VEVENT":
            if not summary_regex.match((element["summary"])):
                new_cal.add_component(element)

    return new_cal.to_ical(False).decode("utf-8").replace("\r\n", "\n")


class ICalHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == f"/{token}":
            try:
                message = filter_ical()
                self.send_response(200)
                self.send_header("Content-Type", "text/calendar;charset=UTF-8")
                self.end_headers()
                self.wfile.write(bytes(message, "utf-8"))
            except:
                self.send_response(503)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


httpd = http.server.HTTPServer(('', 8245), ICalHTTPRequestHandler)
httpd.serve_forever()
