#!/usr/bin/env python3
"""
Module for filtering and obfuscating specific fields in log messages.

This module defines the `filter_datum` function, which is used to
replace the values of specified fields in a log message with a redaction
string, effectively masking sensitive information.

The `filter_datum` function uses regular expressions
to search for the given fields and replaces their
values with the specified redaction.
"""

import logging
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str
) -> str:
    """
    Replaces values of specific fields in a log message with
    a redaction string.

    Arguments:
        fields (List[str]): A list of field names (keys)
                        to obfuscate in the log message.
        redaction (str): The string that will replace the values of
                        the specified fields.
        message (str): The log message that contains the fields
                        to be obfuscated.
        separator (str): The character that separates fields in
                        the log message (e.g., ';' or '&').

    Returns:
        str: A new log message where the specified fields have been redacted.

    Example:
        fields = ["password", "date_of_birth"]
        message = "name=egg;email=eggmin@eggsample.com;
                    password=eggcellent;date_of_birth=12/12/1986;"
        redacted_message = filter_datum(fields, 'xxx', message, ';')
        print(redacted_message)
        # Output: "name=egg;email=eggmin@eggsample.com;
                    password=xxx;date_of_birth=xxx;"
    """
    # Build the regex pattern to match the fields and their values
    pattern = f"({'|'.join(fields)})=([^{separator}]*)"
    # Use re.sub to replace matched values with the redaction
    return re.sub(
        pattern, lambda match: f"{match.group(1)}={redaction}", message
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record by obfuscating sensitive information.

        This method overrides the `format` method of `logging.Formatter`
        to provide additional processing on the log message. It uses the
        `filter_datum` function to replace sensitive information
        in specified fields with a redaction string.

        Parameters:
            record (logging.LogRecord): The log record object containing the
                                        log message and associated metadata.

        Returns:
            str: The formatted log message with sensitive fields obfuscated.

        Example:
            Suppose the original log message is:
                "user=alice;email=alice@example.com;password=secret123;"
            and `self.fields` includes "password" with `self.REDACTION`
            set to "****". After applying `filter_datum`, the
            formatted message would become:
                "user=alice;email=alice@example.com;password=****;"
        """
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR
        )

        return super(RedactingFormatter, self).format(record)
