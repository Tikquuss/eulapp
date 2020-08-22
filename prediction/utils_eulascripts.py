import re
import  fitz

def text_is_valid(text : str):
    return text.strip().rstrip().replace("\n", "").replace("\r", "").replace("\t", "") # != ""

def can_be_subtitle_or_subsubtitle(e : str) :

    regex_subsubtitle = '^\w+\.\w?|^\(?\w+\)\w?'
    regex_subsubtitle_no_romain = '^\w{,1}\.\w?|^\(?\w{,1}\)\w?'
    romain_set = {"i", "v", "x", ".", ")", "("}
    e_strip = e.replace("'", "")
    #print("e_strip",  e_strip)
    m = re.match(regex_subsubtitle, e_strip)
    if m :
        v = e_strip.split(" \n")
        id = v[0]
        if set(id).issubset(romain_set) :
            return "romain"
        else :
            if len(id) <= 3 and re.match(regex_subsubtitle_no_romain, id) :
                if ('.' in id or id[1] == ')') and len(id) == 2 :
                    return "no_romain"


def can_be_title(e : str):
  regex_title = '[0-9]+\. \\n\w?'
  if re.search(regex_title, e) :
      return " \n"
  else :
     regex_title = '[0-9]+\.\w?'
     return " "

def pyMuPDF_clauses_extraction(document):
    doc = fitz.open(document)

    fake_string = '__fake__'
    current = '0.'
    current_title = current
    current_subtitle = ""
    current_subsubtitle = ""
    dico = {}
    dico[current] = []
    for page in doc :
        blocks = page.getText("blocks")
        for line in blocks :
            line = line[4]
            if text_is_valid(line) :
                a = can_be_title(line)
                b = can_be_subtitle_or_subsubtitle(line)
                if a or b :
                    #print("==0", line)
                    v = line.split(a)
                    id = v[0]
                    text = a.join(v[1:])
                    
                    current = id
                    """
                    if a :
                        current_title = id
                        current = id
                    if b == "no_romain" :
                        current_subtitle = id
                        current = (current_title +"." if current_title else "") + id
                    if b == "romain" :
                        current_subsubtitle = id
                        current = (current_title +"." if current_title else "")+ (current_subtitle +"." if current_subtitle else "")+ id
                    """
                    
                    if current in dico.keys():
                        i = 1
                        while id+fake_string+str(i) in dico.keys():
                            i += 1
                        current = id+fake_string+str(i)

                    try :
                        dico[current].append(text)
                        #print(current, current_title, "2 === ",line)
                    except  :
                        dico[current] = [text]
                        #print(current, current_title, "1 === ",line)
                    
                else :
                    #print(repr(line))
                    dico[current].append(line)
                    #print(current, current_title, "3   === ",line)
    
    for k , v in dico.copy().items():
        dico[k] = "\n".join(v)             
    
    return dico