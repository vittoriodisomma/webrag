#--kind python:default
#--web true
import translation
def main(args):
  return { "body": translation.translation(args) }
