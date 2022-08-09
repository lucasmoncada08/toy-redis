class RESPDecoder:
  def __init__(self, connection):
    self.connection = ConnectionBuffer(connection)

  def decode(self):
    """Main function used to evaluate what type of data is recieved"""
    
    data_type_byte = self.connection.read(1)

    if data_type_byte is None:
      return

    if data_type_byte == b"+":
      return self.decode_simple_string()
    elif data_type_byte == b"$":
      return self.decode_bulk_string()
    elif data_type_byte == b"*":
      return self.decode_array()
    else:
      raise Exception(f"Unknown data type byte: {data_type_byte}") 

  def decode_simple_string(self):
    return self.connection.read_until_delimeter(b"\r\n")

  def decode_bulk_string(self):
    string_length = int(self.connection.read_until_delimeter(b"\r\n"))
    data = self.connection.read(string_length)
    assert self.connection.read_until_delimeter(b"\r\n") == b""
    return data

  def decode_array(self):
    result = []
    array_length = int(self.connection.read_until_delimeter(b"\r\n"))

    for _ in range(array_length):
      result.append(self.decode())
    
    return result

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