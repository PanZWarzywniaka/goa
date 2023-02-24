
def get_prompt_from_path(img_path):
    #e.g. from /path/to/dir/lovely dog-1.png
    #return lovely dog
    file_name = img_path.split("/")[-1]
    prompt = file_name.split("-")[0]
    return prompt

if __name__ == "__main__":
    path = "/dir/dir/dir/an abstract interpretation of the search for absolute values and iuris fontes. use simple shapes, art deco style, thin strips, calm warm colours, use 3 colours only, symbolic and minimalistic-1.png"
    prompt = get_prompt_from_path(path)
    print(prompt)
    