class RESPDecoder:
  def __init__(self, connection):
    self.connection = ConnectionBuffer(connection)

  def decode(self):
    """Main function used to evaluate what type of data is recieved"""
    
    data_type_byte = self.connection.read(1)

    if data_type_byte == b"+":
      return self.decode_simple_string()
    else:
      return b"echo"

  def decode_simple_string(self):
    return self.connection.read_until_delimeter(b"\r\n")

class ConnectionBuffer:
  def __init__(self, connection):
    self.connection = connection
    self.buffer = b""
  
  def read(self, buff_size):
    if len(self.buffer) < buff_size:
      data = self.connection.recv(1024)

      if not data:
        return None
      
      self.buffer += data

    data, self.buffer = self.buffer[:buff_size], self.buffer[buff_size:]
    return data

  def read_until_delimeter(self, delimeter):
    while delimeter not in self.buffer:
      data = self.connection.recv(1024)

      if not data:
        return None

      self.buffer += data

    data_before_delim, delim, self.buffer = self.buffer.partition(delimeter)
    return data_before_delim