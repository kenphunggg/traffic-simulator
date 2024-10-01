import os

class Message:
  ColorRedCode = "\033[1;31m"
  ColorGreenCode = "\033[1;32m"
  ColorBlueCode = "\033[1;34m"
  ColorYellowCode = "\033[1;33m"
  ColorMagnetaCode = "\033[1;35m"
  ResetCode = "\033[0m"

  @staticmethod
  def RedMessage(message):
    os.system(f"echo '{Message.ColorRedCode}{message}{Message.ResetCode}'")

  @staticmethod
  def GreenMessage(message):
    os.system(f"echo '{Message.ColorGreenCode}{message}{Message.ResetCode}'")

  @staticmethod
  def BlueMessage(message):
    os.system(f"echo '{Message.ColorBlueCode}{message}{Message.ResetCode}'")

  @staticmethod
  def YellowMessage(message):
    os.system(f"echo '{Message.ColorYellowCode}{message}{Message.ResetCode}'")

  @staticmethod
  def MagnetaMessage(message):
    os.system(f"echo '{Message.ColorMagnetaCode}{message}{Message.ResetCode}'")

  @staticmethod
  def DefaultMessage(message):
    os.system(f"echo '{message}'")

  

# y = msg.MagnetaMessage("toi la thai")