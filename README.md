# This repository has been migrated to codeberg.org
See [here](https://codeberg.org/PatrickJosh/icalfilter).

# icalfilter

This little script can be used to filter events in an ical file by their summary.
A regular expression is used to do this.
The filtered ical is made available via a small web server.

## Configuration

The `icalfilter.conf` is used to configure the script:

- `original_url:`: URL of the source ical file
- `summary_regex`: The regular expression used to filter the summary. Events whose summary matches the regex get removed.
- `token`: Token that is needed to access the new ical file, see below.

If you enter all the needed information and run the script, you can access the new ical file at `localhost:8245/$token`, where `$token` is the token set in the configuration.

## Dependencies

The script uses: 

- [icalendar](https://github.com/collective/icalendar)
