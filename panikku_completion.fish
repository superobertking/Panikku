set -l datasets hiragana katakana hangul jis jiskana

function __fish_panikku_rootcond -V datasets
    not __fish_seen_subcommand_from $datasets
end

# Disable file globally (but does not affect --voice)
complete -c panikku -f

# Usable in both global and each dataset
complete -c panikku -s h -l help -d 'Show help'

# Global options
complete -c panikku -n "__fish_panikku_rootcond" -l no-say -d 'Say the word using TTS after each quiz'
complete -c panikku -n "__fish_panikku_rootcond" -l say-first -d 'Say the word before each quiz. Otherwise, say it after each quiz.'
complete -c panikku -n "__fish_panikku_rootcond" -l notify-wrong -d "Notify wrong answer by saying 'wrong answer'."
complete -c panikku -n "__fish_panikku_rootcond" -l typing -d 'Typing test instead of default romanization quiz'
complete -c panikku -n "__fish_panikku_rootcond" -l reverse -d 'Reverse romanization and character'
complete -c panikku -n "__fish_panikku_rootcond" -l recitation -d 'Play sound first and do not show the character (implies --say and --say-first)'

function __fish_panikku_say_args
    say -v '?' | string replace -r '^(.*\S)\s+([a-z]{2}_.*)$' '$1	$2'
end
complete -c panikku -n "__fish_panikku_rootcond" -s v -l voice -d 'Override voice choice' -x -a "(__fish_panikku_say_args)"

# Positional argument
complete -c panikku -n "__fish_panikku_rootcond" -k -a "$datasets" -d 'Datasets'

# Supported simple modules
function __fish_panikku_select_from
    set -l cmd (commandline -pxc)[2..]
    for s in $argv
        # hack for a bug in fish 4.0.2 __fish_seen_subcommand_from...
        # https://github.com/fish-shell/fish-shell/commit/4412164fd4e80376f246a6c2eacec8c61fea4633
        if ! contains -- $s $cmd; echo $s; end
    end
end
complete -c panikku -n "__fish_seen_subcommand_from hiragana katakana" \
    -a '(__fish_panikku_select_from normal dakuon yoon_normal yoon_dakuon)' -d 'Kana'

complete -c panikku -n "__fish_seen_subcommand_from jis" \
    -a 'us jis' -d 'Keyboard'
complete -c panikku -n "__fish_seen_subcommand_from jiskana" \
    -a '(__fish_panikku_select_from us)' -d 'Keyboard'

function __fish_panikku_hangul_args
    echo "\
consonant	All Consonants
vowel		All Vowels
patchim		Non-empty Patchims
syllable	All Hangul (LV+LVT)
consonant:	Custom Consonants
vowel:		Custom Vowels
patchim:	Custom Patchims
syllable:	Custom Hangul
lv		All LV  (leading+vowel)
lvt		All LVT (leading+vowel+patchim)
all		All Hangul (LV+LVT)
"
end

complete -c panikku -n "__fish_seen_subcommand_from hangul" \
    -k -a '(__fish_panikku_hangul_args)'

# Handle "consonant:setname" scenario
function __fish_panikku_token_colon -a subcommand
    set -l token (commandline -pct)
    string match -rq -- "^$subcommand:" $token
end

function __fish_panikku_gen_arg_description -a prefix desc
    for s in $argv[3..]
        echo "$prefix:$s	$desc"
    end
end
function __fish_panikku_consonant_args
    __fish_panikku_gen_arg_description consonant 'Consonant' plain tense aspirated
    __fish_panikku_gen_arg_description consonant 'Alias' base double asp
    __fish_panikku_gen_arg_description consonant 'Group' all
end
function __fish_panikku_vowel_args
    __fish_panikku_gen_arg_description vowel 'Vowel' base ybase double
    __fish_panikku_gen_arg_description vowel 'Group' single all
end
function __fish_panikku_patchim_args
    __fish_panikku_gen_arg_description patchim 'Patchim' single double
    __fish_panikku_gen_arg_description patchim 'Group' nonempty all
end

complete -c panikku -n "__fish_seen_subcommand_from hangul" -n "__fish_panikku_token_colon consonant" \
    -k -a "(__fish_panikku_consonant_args)"
complete -c panikku -n "__fish_seen_subcommand_from hangul" -n "__fish_panikku_token_colon vowel" \
    -k -a "(__fish_panikku_vowel_args)"
complete -c panikku -n "__fish_seen_subcommand_from hangul" -n "__fish_panikku_token_colon patchim" \
    -k -a "(__fish_panikku_patchim_args)"


# Handle syllable:<consonant..>*<vowel..>[*<patchim..>] scenario

function __fish_panikku_syllable_split -a n
    set -l token (commandline -pct)
    string match -rq -- '^syllable(?<split0>:)[^*+]*([^*+](?<split1>[*+])[^*+]*([^*+](?<split2>[*+])[^*+]*)?)?$' $token
    test (string length "$split0$split1$split2") -eq $n
    # Or use separate match regex:
    # string match -rq -- '^syllable:[^*+]*$' (commandline -pct)
    # string match -rq -- '^syllable:[^*+]+[*+][^*+]*$' (commandline -pct)
    # string match -rq -- '^syllable:[^*+]+[*+][^*+]+[*+][^*+]*$' (commandline -pct)
end

# '*' and '\*' do not work well..
set -l splitsym '+'  # '\*'
set -l consonant_options plain tense aspirated base double asp all
set -l vowel_options base ybase double single all
# set -l patchim_options single double nonempty all

function __fish_panikku_syllable_args_consonant_part -V splitsym -a desc
    for s in syllable:$argv[2..]$splitsym
        echo "$s	$desc"
    end
end
function __fish_panikku_syllable_args_consonant
    __fish_panikku_syllable_args_consonant_part 'Consonant Part' plain tense aspirated
    __fish_panikku_syllable_args_consonant_part 'Consonant Part Alias' base double asp
    __fish_panikku_syllable_args_consonant_part 'Consonant Part Group' all
end
function __fish_panikku_syllable_args_vowel_part -V splitsym -V consonant_options -a desc tail
    for s in syllable:$consonant_options$splitsym$argv[3..]$tail
        echo "$s	$desc"
    end
end
function __fish_panikku_syllable_args_vowel
    __fish_panikku_syllable_args_vowel_part 'Vowel Part' '' base ybase double
    __fish_panikku_syllable_args_vowel_part 'Vowel Part Group' '' single all
    __fish_panikku_syllable_args_vowel_part 'Vowel Part with Patchim' '+' base ybase double
    __fish_panikku_syllable_args_vowel_part 'Vowel Part Group with Patchim' '+' single all
end
function __fish_panikku_syllable_args_patchim_part -V splitsym -V consonant_options -V vowel_options -a desc
    for s in syllable:$consonant_options$splitsym$vowel_options$splitsym$argv[2..]
        echo "$s	$desc"
    end
end
function __fish_panikku_syllable_args_patchim
    __fish_panikku_syllable_args_patchim_part 'Patchim Part' single double
    __fish_panikku_syllable_args_patchim_part 'Patchim Part Group' nonempty all
end

complete -c panikku -n "__fish_seen_subcommand_from hangul" -n "__fish_panikku_syllable_split 1" \
    -k -a "(__fish_panikku_syllable_args_consonant)"
complete -c panikku -n "__fish_seen_subcommand_from hangul" -n "__fish_panikku_syllable_split 2" \
    -k -a "(__fish_panikku_syllable_args_vowel)"
complete -c panikku -n "__fish_seen_subcommand_from hangul" -n "__fish_panikku_syllable_split 3" \
    -k -a "(__fish_panikku_syllable_args_patchim)"
