IFS=

declare -a languages=("intel" "att" "mips_asm" "mips_mml" "riscv")
declare -a bases=("dec" "dec" "hex" "hex" "hex")
declare -a vm=("Intel" "Intel" "MIPS" "MIPS" "RISCV")

for index in "${!languages[@]}"
do
    echo "${languages[$index]}"
    INSTALL_CONTENT=$(cat templates/install_template.txt | sed -e "s/KERNEL_TEMPLATE_NAME/${languages[$index]}/g")
    echo ${INSTALL_CONTENT} > ${languages[$index]}/install.py

    UNINSTALL_CONTENT=$(cat templates/uninstall_template.txt | sed -e "s/KERNEL_TEMPLATE_NAME/${languages[$index]}/g")
    echo ${UNINSTALL_CONTENT} > ${languages[$index]}/uninstall.py

    cp templates/kernel_template.txt ${languages[$index]}/kernel.py
    NAME=`echo ${languages[$index]:0:1} | tr '[a-z]' '[A-Z]'`${languages[$index]:1}
    sed -i '' -e "s/FLAVOR/${languages[$index]}/g" -e "s/NAME/${NAME}/g" -e "s/BASE/${bases[$index]}/g" -e "s/VM/${vm[$index]}/g" ./${languages[$index]}/kernel.py

    MAIN_CONTENT=$(cat templates/main_template.txt | sed -e "s/NAME/${NAME}/g")
    echo ${MAIN_CONTENT} > ${languages[$index]}/__main__.py

    cp templates/init_template.txt ${languages[$index]}/__init__.py
done
