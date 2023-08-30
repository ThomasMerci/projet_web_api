import openai
"""
GITHUB_ACTIONS=true pip install auto-gptq
pip3 install git+https://github.com/huggingface/transformers
unset CUDA_VERSION && pip install auto-gptq==0.2.0

from transformers import AutoTokenizer, pipeline, logging
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig

def model(prompt):
    model_name_or_path = "TheBloke/Llama-2-13B-chat-GPTQ"
    model_basename = "model"
    use_triton = False
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
    model = AutoGPTQForCausalLM.from_quantized(model_name_or_path,
            model_basename=model_basename,
            use_safetensors=True,
            trust_remote_code=True,
            device="cuda:0",
            use_triton=use_triton,
        quantize_config=None)
    
    system_message = "Répondez toujours de manière aussi utile que possible, tout en étant prudent. Vos réponses ne doivent pas inclure de contenu nuisible, contraire à l'éthique, raciste, sexiste, toxique, dangereux ou illégal. Assurez-vous que vos réponses sont impartiales socialement et positives dans leur nature. Si une question n'a pas de sens ou n'est pas cohérente sur le plan factuel, expliquez pourquoi au lieu de répondre quelque chose d'incorrect. Si vous ne connaissez pas la réponse à une question, ne partagez pas d'informations fausses, s'il vous plaît."
    prompt_template=f'''[INST] <<SYS>>
    {system_message}
    <</SYS>>
    {prompt} [/INST]'''  
    
    pipe = pipeline( "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.95,
        repetition_penalty=1.15)

    reponse = pipe(prompt_template)[0]['generated_text']
    reponse= reponse.split('[/INST]')[-1].lstrip()
    print(reponse)
    return reponse
"""

def retour_texte(prompt, cle, dt):
    try:
        API_KEY = cle
        if not API_KEY:
            raise ValueError("pas de clé")
        openai.organization = "org-3L3lAYc8qcefpgD8i2jERLbL"
        openai.api_key = API_KEY
        response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        max_tokens=1000
        )
        data = response["choices"][0]["text"].strip() 
        return data
    except:
        reponse2 = f" {dt['city']}, {dt['temp']}°C, max {dt['temp_max']}°C,  min{dt['temp_min']}°C, humidité {dt['humidity']}%, pression{dt['pressure']} hPa, couverture nuageuse de {dt['cloudiness']}%, levé du soleil {dt['sunrise']}, vent de {dt['wind']} m/s"
        return reponse2



