#! /bin/bash
> requirements.txt

while IFS= read -r package; do
    package=$(echo "$package" | xargs)
    [ -z "$package" ] && continue
    result=$(pip freeze | grep -i "^${package}==")

    if [ -n "$result" ]; then
        echo "$result" >> requirements.txt
    fi
done < .lib

echo "requirements.txt updated!"
