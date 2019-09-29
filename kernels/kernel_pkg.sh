IFS=

declare -a languages=("intel" "att" "mips_asm" "mips_mml" "riscv")
declare -a bases=("dec" "dec" "hex" "hex" "hex")
declare -a vm=("Intel" "Intel" "MIPS" "MIPS" "RISCV")

for index in "${!languages[@]}"
do
    echo "${languages[$index]}"
    INSTALL_CONTENT=$(cat install_template.txt | sed -e "s/KERNEL_TEMPLATE_NAME/${languages[$index]}/g")
    echo ${INSTALL_CONTENT} > ${languages[$index]}_kernel/install.py

    UNINSTALL_CONTENT=$(cat uninstall_template.txt | sed -e "s/KERNEL_TEMPLATE_NAME/${languages[$index]}/g")
    echo ${UNINSTALL_CONTENT} > ${languages[$index]}_kernel/uninstall.py

    NAME=`echo ${languages[$index]:0:1} | tr  '[a-z]' '[A-Z]'`${languages[$index]:1}
    KERNEL_CONTENT=$(cat kernel_template.txt | sed -e "s/FLAVOR/${languages[$index]}/g" | sed -e "s/FLAVOR/${languages[$index]}/g" | sed -e "s/NAME/${NAME}/g" | sed -e "s/BASE/${bases[$index]}/g" | sed -e "s/VM/${vm[$index]}/g" )
    echo ${KERNEL_CONTENT} > ${languages[$index]}_kernel/kernel.py

    MAIN_CONTENT=$(cat main_template.txt | sed -e "s/NAME/${NAME}/g")
    echo ${MAIN_CONTENT} > ${languages[$index]}_kernel/__main__.py
done
