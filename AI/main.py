import openai
import os, json

let = lambda x, y: y
do = lambda *args: tuple(map(lambda x: x, args))[-1]

openai.api_key = " YOUR API KEY "

# MUT - ABSTRACTION
join_dicts = lambda d1, d2: do(
    d1.update(d2),
    d1)

# PURE
main = lambda: (
    do(f := open('data_base.json', 'r'), data_base := json.loads(f.read()), f.close(), 
        let(prompt := input('> ').strip().lower(),
            do(print(data_base[prompt])
               , main()) if prompt in data_base.keys() else (
                let(response := openai.Completion.create(engine="text-babbage-001"
                                                        , prompt=prompt
                                                        , max_tokens=50
                                                        , n=1
                                                        , stop=None
                                                        , temperature=0.5,).choices[0].text
                    , do(
                        print(response),
                        do(
                            f := open('data_base.json', 'w'),
                            f.write(json.dumps(join_dicts(data_base, {prompt: response}))),
                            f.close()
                        ),
                        main()))))))

do(
    f := open('data_base.json', 'w'),
    f.write('{}'),
    f.close(),
    main()
) if not ('data_base.json' in os.listdir()) else main()
