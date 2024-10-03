# e-ticaretHackathon
LLMCini Takımı Teknofest e-Ticaret Hackathon reposu


![alt text](demo.jpeg)

## Kullanım

### 
```
$git clone https://github.com/LLMCini/e-ticaretHackathon
$cd e-ticaretHackathon
```

#### Gerekliliklerin yüklenmesi
```
pip install -r requirements.txt
```

#### Modellerin import edilmesi

> [!TIP]
> Modelleri indirip kopyalamamız gereken dizinler aşağıda verilmiştir.
> 
> /e-ticaretHackathon/ComfyUI/models/[grounding-dino/](https://huggingface.co/alexgenovese/background-workflow/blob/1cbf8c24aa8a2e8d5ca6871800442b35ff6f9d48/groundingdino_swint_ogc.pth) klasörüne indirdiğiniz model dosyasının kopyalayın.  
> /e-ticaretHackathon/ComfyUI/models/[ipadapter/](https://huggingface.co/h94/IP-Adapter/blob/main/sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors) klasörüne indirdiğiniz model dosyasının kopyalayın.  
> /e-ticaretHackathon/ComfyUI/models/[controlnet/](https://huggingface.co/stabilityai/control-lora/blob/main/control-LoRAs-rank256/control-lora-depth-rank256.safetensors) klasörüne indirdiğiniz model dosyasının kopyalayın.  
> /e-ticaretHackathon/ComfyUI/models/[checkpoints/](https://civitai.com/models/207750/moomooe-commerce) klasörüne indirdiğiniz model dosyasının kopyalayın.  
> /e-ticaretHackathon/ComfyUI/models/[clip_vision/](https://huggingface.co/laion/CLIP-ViT-H-14-laion2B-s32B-b79K/blob/main/open_clip_pytorch_model.safetensors) klasörüne indirdiğiniz model dosyasının kopyalayın.  
#### !UYARI clip_vision dosyasına modelin adını değiştirerek yükleyin "LIP-ViT-H-14-laion2B-s32B-b79K.safetensors"  
```
$ mv open_clip_pytorch_model.safetensors LIP-ViT-H-14-laion2B-s32B-b79K.safetensors
```
_______

 ### Gerekliliklerin yüklenmesi
```pip install -r requirements.txt```

### S.S.S
> Veri seti paylaşmışsınız modeli tekrar eğitmem gerekiyor mu?  
> Hayır. LLM modelini paylaştığımız veri seti ile Finetune ettik. Tekrar eğitim için kullanılmasına gerek yok.

> Modele sadece Finetuning mi uyguladınız?
> Hayır. 'unsloth.Q8_0.gguf' adında quantize edilmiş bir model de mevcut.
> HuggingFace reposunu kontrol edebilirsiniz.


```git
==((====))==  Unsloth - 2x faster free finetuning | Num GPUs = 1
   \\   /|    Num examples = 3,011 | Num Epochs = 1
O^O/ \_/ \    Batch size per device = 2 | Gradient Accumulation steps = 4
\        /    Total batch size = 8 | Total steps = 80
 "-____-"     Number of trainable parameters = 83,886,080
 [80/80 02:02, Epoch 0/1]
```
```git
Step	Training Loss
1	2.040200
2	1.996800
3	2.047000
       .
       .
       .

79	0.458500
80	0.435000
```




## Kullanılan Modellerin Lisansları
> [!WARNING]
> STABILITY AI CONTROL-LORA COMMUNITY LICENSE AGREEMENT  
> Ticari amaçlı kullanımlarda dikkat edilmesi gereken maddeler  
> [MADDE 2](https://huggingface.co/stabilityai/control-lora/blame/1c1c7bcb56224c202c1e624c2128f97c48cebcea/LICENSE.MD) -AYLIK ANLIK AKTİF KULLANICI SAYISI 1.000.000 VE ÜSTÜNDE OLMASI TİCARİ LİSANS GEREKTİRİR-

> Stability AI CreativeML Open RAIL++-M License 
> Ticari amaçlı kullanımlarda dikkat edilmesi gereken madde yoktur.

> Apache 2.0
> Ticari amaçlı kullanımlarda dikkat edilmesi gereken madde yoktur.

> MIT
> Ticari amaçlı kullanımlarda dikkat edilmesi gereken madde yoktur.

> META LLAMA 3 COMMUNITY LICENSE
> [MADDE 2](https://huggingface.co/meta-llama/Meta-Llama-3-8B/blob/main/LICENSE) -Aylık aktif kullanıcıları, önceki takvim ayında 700 milyondan fazla aylık aktif kullanıcıya sahipse lisans talep edilmelidir.-

