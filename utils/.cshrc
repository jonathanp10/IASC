############################################################################################
# PRE section ... DON'T MODIFY BETWEEN THESE LINES and keep at the BEGINNING of the .cshrc #

setenv _SEG_DURING_CSHRC_READ_ 1

if (-r "/org/seg/environment/cshrc/cshrc.header") source "/org/seg/environment/cshrc/cshrc.header"

# PRE section ... DON'T MODIFY BETWEEN THESE LINES and keep at the BEGINNING of the .cshrc #
############################################################################################


# Global completions

if ($?prompt) source /org/seg/environment/complete/.complete

if ($?_SEG_INHERIT_ENV_) then
    if ($?prompt) then
        if (-r ~/.alias)                                        source ~/.alias
        if (-r ~/.complete)                                     source ~/.complete
    endif
    unsetenv _SEG_INHERIT_ENV_
else
    if (  $?prompt && -r "$HOME/.cshrc.user")               source "$HOME/.cshrc.user"
    if (! $?prompt && -r "$HOME/.cshrc.user.no_prompt")     source "$HOME/.cshrc.user.no_prompt"
endif





###########################################################################################
# POST section ... DON'T MODIFY BETWEEN THESE LINES and keep at the END of the .cshrc     #

if (-r "/org/seg/environment/cshrc/cshrc.footer") source "/org/seg/environment/cshrc/cshrc.footer"

unsetenv _SEG_DURING_CSHRC_READ_

# POST section ... DON'T MODIFY BETWEEN THESE LINES and keep at the END of the .cshrc     #
###########################################################################################
