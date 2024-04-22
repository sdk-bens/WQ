import subprocess
import sys
import torch
from hqq.core.quantize import BaseQuantizeConfig
from huggingface_hub import snapshot_download
from transformers import AutoConfig
from src.build_model import OffloadConfig, QuantConfig, build_model

# Clone the repository
subprocess.run(["git", "clone", "https://github.com/dvmazur/mixtral-offloading.git", "--quiet"])

# Install the requirements
subprocess.run(["pip", "install", "-q", "-r", "mixtral-offloading/requirements.txt"])

# Download the model
subprocess.run(["huggingface-cli", "download", "lavawolfiee/Mixtral-8x7B-Instruct-v0.1-offloading-demo", "--quiet", "--local-dir", "Mixtral-8x7B-Instruct-v0.1-offloading-demo"])

sys.path.append("mixtral-offloading")


def build_model():
    """
    Clones a repository, installs requirements, downloads a model,
    and sets up and configures a model based on specified parameters.

    Returns:
    - model: A configured and initialized model ready for use.
    """
    config = AutoConfig.from_pretrained(quantized_model_name)

    quantized_model_name = "lavawolfiee/Mixtral-8x7B-Instruct-v0.1-offloading-demo"
    state_path = "Mixtral-8x7B-Instruct-v0.1-offloading-demo"
    # Change this to 5 if you have only 12 GB of GPU VRAM #####
    offload_per_layer = 4
    num_experts = config.num_local_experts
    offload_config = OffloadConfig(
    main_size=config.num_hidden_layers * (num_experts - offload_per_layer),
    offload_size=config.num_hidden_layers * offload_per_layer,
    buffer_size=4,
    offload_per_layer=offload_per_layer,
    )


    attn_config = BaseQuantizeConfig(
        nbits=4,
        group_size=64,
        quant_zero=True,
        quant_scale=True,
    )
    attn_config["scale_quant_params"]["group_size"] = 256


    ffn_config = BaseQuantizeConfig(
        nbits=2,
        group_size=16,
        quant_zero=True,
        quant_scale=True,
    )
    quant_config = QuantConfig(ffn_config=ffn_config, attn_config=attn_config)
    model = build_model(
        device= torch.device("cuda:0"),
        quant_config=quant_config,
        offload_config=offload_config,
        state_path=state_path,
    )
    return model
