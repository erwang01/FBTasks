def split_text(text, max_char):
    text_list = text.split (". ")
    message = [""]
    index = 0
    for snippet in text_list:
        if message[index] == "":
            message[index] = message[index] + snippet
        elif len(message[index])> max_char-5:
            message.append(snippet)
            index += 1
    for i in range(1,index+1):
        message[i-1] = message[i-1] + " (" + str(i) + "/" + str(index+1) + ")"

    return message

def test_split_text(max_char):
    text = "Douglas MacArthur (26 January 1880 – 5 April 1964) was an American five-star general and Field Marshal of the Philippine Army. He was Chief of Staff of the United States Army during the 1930s and played a prominent role in the Pacific theater during World War II. He received the Medal of Honor for his service in the Philippines Campaign, which made him and his father Arthur MacArthur Jr., the first father and son to be awarded the medal. He was one of only five men ever to rise to the rank of General of the Army in the US Army, and the only man ever to become a field marshal in the Philippine Army."
    splits = split_text(text, max_char)
    errors = 0
    for split in splits:
        print(split)
        if len(split) > max_char:
            errors += 1
    
    print(errors)

if __name__ == "__main__":
    test_split_text(200)