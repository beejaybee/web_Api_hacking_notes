# grep
 - grep password file.txt
 - This tells grep to search for the string password in the file file.txt

 - grep -E "^\S+\s+\S+\s+\S+$" DIRECTORY/nmap > DIRECTORY/nmap_cleaned
 - You need to parse the JSON file from crt.sh. You can do this with jq, a command line utility that processes JSON. If we examine the JSON output file from crt.sh, we can see that we need to extract the name_value field of each certificate item to extract domain names. This command does just that: 
 ** $ jq -r ".[] | .name_value" $DOMAIN/crt **