echo "List of available mopdels to download:"
echo "https://catalog.ngc.nvidia.com/orgs/nvidia/collections/nemo_asr\n"
echo "Now it would be downloaded the model: stt_ru_quartznet15x5_1.0.0rc1 ok?"
read -p "y/n: " answer
if [ "$answer" = "y" ]; then
    wget --content-disposition https://api.ngc.nvidia.com/v2/models/nvidia/nemo/stt_ru_quartznet15x5/versions/1.0.0rc1/zip -O stt_ru_quartznet15x5_1.0.0rc1.zip
    unzip stt_ru_quartznet15x5_1.0.0rc1.zip
    rm stt_ru_quartznet15x5_1.0.0rc1.zip
    echo "Model downloaded and extracted"
else
    echo "Model not downloaded"
fi
