import logging
import click

from .dbimport import dbimport as dbimport_cmd

@click.group()
@click.option('--loglevel', default='INFO', help='level of logging')
@click.pass_context
def base(ctx, loglevel):
    setup_logging(loglevel)
    ctx.obj = {}


def setup_logging(loglevel="INFO"):
    """
    Set up logging
    :param loglevel: loglevel to use, one of ERROR, WARNING, DEBUG, INFO (default INFO)
    :return:
    """
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
	raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level,
			format='%(levelname)s %(asctime)s %(funcName)s - %(message)s')
    logging.debug("Started log with loglevel %(loglevel)s" % {"loglevel": loglevel})

base.add_command(dbimport_cmd)
