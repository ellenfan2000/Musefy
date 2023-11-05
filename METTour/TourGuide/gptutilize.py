import os
import openai
import json
import ast

openai.api_key = os.getenv("OPENAI_API_KEY")

def gen_message(time, date, curatorial, period, artist, theme, age):
    prompt = "Instruction: Now please act as my personal museum tour guide. Plan a navigation route of 10 pieces of art at\
        The Metropolitan Museum of Art. The route should be made up of an interesting sequence of \
        artworks based on my \“input requirements\” and \“output requirements\” stated below.\n\
        Context: I am visiting The Metropolitan Museum of Art in New York, United States. The \
        museum is so large and consists so many artworks in different areas. You can see the full \
        list of open-access artworks here: \ https://www.metmuseum.org/art/collection/search?showOnly=openAccess&searchField=All&sortBy=relevance. \
        Also there are so many art from different curatorial areas. See here: \
        https://www.metmuseum.org/art/the-collection#browse-by. Also, there are so many themes to \
        be considered. See here: https://www.metmuseum.org/art/the-collection#browse-by. \
        I am totally lost and don't know where to start from and don't know how to navigate my way \
        to make my trip worth it. Besides, I not only want to see a list of arbitrarily chosen art. \
        I want to immerse myself in the story behind the art piece. Ideally, I want to discover a \
        complete storyline. For example, one vase from Asian pottery exhibition was actually \
        present in another Western canvas oil paint. I would love to see the vase first and see the \
        oil paint next. For another example, Van Gogh drew a lot of paintings before and after he \
        lost his love(a life-turning point). I would love to first see those drawn before he lost his love \
        and those after. I would love to learn if there are any emotional differences, style \
        differences, etc.. \n  \
        Input requirements: I plan to visit for {} on {}. I am most interested in \
        appreciating art pieces from {} from the timespan {}. But I am not limited to \
        these. I am also interested in other artworks from other curatorial areas that are related to \
        them. I want to appreciate as many art pieces by {} as possible. I hope this interesting \
        tour can have this {}. I am age {}. If there is some art piece that is suitable for my \
        age I would love to see it. \
        On top of the previous requirements, please plan the tour with a storyline. For example, \
        I first see the self-portrait of Van Gogh. Tell me the story of why he lost his ear. Tell me \
        what is the mood and style of the portrait. Tell me if it is related to another art piece in the \
        same museum. If it is related, please navigate my way to that art piece. If you don't have \
        the detailed information and story behind this art piece, please give me the link to the \
        official website so that I can see the official introduction.\n \
        Output requirements:\n\
        A json file that contains the following elements.\
        Elements:\
        Intro: The theme of today's route with an eye-catching and exciting introduction \
        of no more than 5 sentences of what's interesting about it.\
        ArtPiece: The art piece's name\
        Artist: The artist who created the piece\
        Year: The year the piece was created\
        Geo: The region (country or area) the piece was created \
        Story: Within 10 sentences, tell the story behind why you take me here.\
        Related: At least 1 related art works \
        StopTime: Recommended appreciation time: 5 minutes to 30 minutes. \
        OfficialLink: Please provide a link to the official website where I can play the audio \
        or video in the official website of MET. \
        Nextstep: Within 10 sentences, excites me by telling me what's interesting about this art piece. \
        Please make sure to tell me how it's related to the next stop you are \
        taking me to. \
        ".format(time, date, curatorial, period, artist, theme, age)

    messages=[{"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI.\n Knowledge cutoff: 2021-09\nCurrent date: 2023-11"},
            {"role": "user", "content": prompt}]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        max_tokens=3100,  # You can adjust this value to get longer responses
        # temperature=0
    )

    myres=[]
    content_string = response.choices[0].message["content"]
    print(content_string)
    try:
        d = json.loads(content_string)
        myres.append(d)
        print(d)
    except json.JSONDecodeError as e:
        print(f"Error parsing string into dictionary: {e}")

    for i in range(2):
        messages.append({"role": "assistant", "content": response.choices[0].message["content"]})
        messages.append({"role": "user", "content": "Tell me more art pieces."})
        # Send the second message with conversation history
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            # temperature=0
            # max_tokens=3100 
        )
        content_string = response.choices[0].message["content"]
        print(content_string)
        try:
            d = json.loads(content_string)
            myres.append(d)
            print(d)
        except json.JSONDecodeError as e:
            print(f"Error parsing string into dictionary: {e}")
    
    return myres

    # print(completion)
    

if __name__ == "__main__":
    print(gen_message("3h", "12.3", "Europe", "1700-2000", "Van gohn", "happy", "24"))
    # print("I am delighted to be your personal museum tour guide at The Metropolitan Museum of Art. Today, I have planned an exciting route with a storyline that will take you on a journey to explore the art pieces from Asian countries between 1900-2000, while also incorporating artworks from other curatorial areas that are related to them. Additionally, I have carefully included as many Van Gogh artworks as possible, taking into consideration your preferences and time limit. Let's embark on this immersive tour and discover the world of art together!\n\n1. Intro: Welcome to \"Harmony in Diversity: Exploring Asian Art through Time and Space\". This engaging route will allow you to appreciate the art pieces from Asian countries between 1900-2000, providing insight into their rich history, diverse cultures, and artistic evolution. Along the way, we will also encounter related artworks from different curatorial areas, creating a cohesive and captivating journey through the museum.\n\n2. Name: \"Self-Portrait with Bandaged Ear\"\n\n3. Artist: Vincent van Gogh\n\n4. Year: 1889\n\n5. Geo: France\n\n6. Story: This self-portrait by Vincent van Gogh holds a significant story behind it. Van Gogh suffered from severe mental health issues, and during a breakdown in December 1888, he famously cut off a part of his left ear. In this portrayal, created after the incident, he captured himself with a bandaged ear, conveying his introspection and turmoil. The portrait showcases van Gogh's mastery in capturing emotions through vivid brushstrokes and intense colors. While there aren't any directly related artworks within the museum, this self-portrait enables us to appreciate the artist's personal struggles and the impact they had on his artistic expression.\n\n7. Related: While there are no specific related artworks within the museum, I recommend exploring \"Starry Night,\" another iconic painting by van Gogh, which is not a part of The Metropolitan Museum of Art collection but can be admired in the Museum of Modern Art (MoMA) located nearby. \"Starry Night\" showcases a different period in van Gogh's life, where he established his unique style despite battling mental and emotional challenges.\n\n8. StopTime: Recommended appreciation time for \"Self-Portrait with Bandaged Ear\" is approximately 10-15 minutes.\n\n9. OfficialLink: [Official Website Link for \"Self-Portrait with Bandaged Ear\"](https://www.metmuseum.org/art/collection/search/436535)\n\n10. Nextstep: After delving into the emotional intensity of \"Self-Portrait with Bandaged Ear,\" our next stop will take us to the \"Japanese Bamboo Art: The Abbey Collection.\" This exhibition showcases the incredible craftsmanship and artistic techniques employed in creating intricate bamboo artworks. From delicate baskets to sculptural masterpieces, this collection highlights the beauty and versatility of this natural material. The connection to van Gogh lies in his admiration for Japanese art and the influence it had on his own artistic development. Prepare to be astounded by the intricate beauty and artistic prowess of the Japanese Bamboo Art collection.")