def compress_message(msg):
    compressed_msg = ""
    i = 0

    while i < len(msg):
        char = msg[i]
        count = 1

        while i + 1 < len(msg) and msg[i] == msg[i + 1]:
            count += 1
            i += 1

        if count > 1:
            compressed_msg += char + str(count)
        else:
            compressed_msg += char

        i += 1

    return compressed_msg

user_input = input("Enter the message to compress: ")
compressed_output = compress_message(user_input)
print("Compressed message:", compressed_output)
