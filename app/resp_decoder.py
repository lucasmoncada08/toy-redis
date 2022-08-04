class RESPDecoder:
  def __init__(self, connection):
    self.connection = connection
    self.buffer = b""

  def decode(self):
    """Main function used to evaluate what type of data is recieved"""
    
    data_type_byte = self.read(1)

    return b"echo"

  def read(self, buff_size):
    if len(self.buffer) < buff_size:
      data = self.connection.recv(1024)

      if not data:
        return None
      
      self.buffer += data

      data, self.buffer = self.buffer[:buff_size], self.buffer[buff_size:]
      return data

    # if data_type_byte == b"+":
    #   return 