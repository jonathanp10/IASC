set tabpagemax=100      " change tab-limit
set guitablabel=%t\%M   " Short tab label
set nocompatible        " no need to be compatible with VI
set modelines=0         " Prevents security exploits that may be done when modelines is used
colorscheme desert      " awesome colorscheme
syntax on               " syntax highlighted on
syntax enable           " enable syntax processing
set nowrap              "
set tabstop=3           " number of visual spaces per TAB
set softtabstop=3       " number of spaces in tab when editing
set shiftwidth=3        " number of spaces for each step of autoident 
set expandtab           " tabs are spaces
set number              " show line numbers
set showcmd             " show command in bottom bar
set ch=2                " Make command line two lines high
set cursorline          "
set textwidth=0         " avoid automatic word wrapping, nowrap was not enough
set ignorecase          " case insensitive search (default is case sensitive)
set smartcase           " search is case-sensitive if an uppercase if the search pattern contains an uppercase letter 
set hlsearch            " highlight search matches
set incsearch           " searches from the first input and refines search as you write more letters
set wrapscan            " This is the default option, search wraps at the bottom
set wildmenu            "
set wildignore=*.dll,*.o,*.obj,*.bak,*.exe,*.pyc,*.jpg,*.gif,*.png
set wildmode=list:longest " turn on wild mode huge list
set backup                   "
set backupdir=~/.vim/backup  " directory for ~backup files 
set directory=~/.vim/tmp     " directory for swp files
set showmatch                 "
set autoindent cindent        " Abbreviations work with this settings 
set clipboard+=noautoselect   "
set clipboard+=unnamed        "
set clipboard+=unnamedplus    "
set autochdir                 "
nnoremap <C-a> [[v<S-g>         
inoremap <C-a> <Esc>[[v<S-g>
nnoremap <C-s> :w<CR>
inoremap <C-s> <ESC>:w<CR>
nnoremap <C-z> u
inoremap <C-z> <Esc>u<Ins>
vnoremap <C-x> "+x      
vnoremap <C-c> "+y
cnoreabbrev <expr> X getcmdtype() == ":" && getcmdline() == 'X' ? 'x' : 'X'
cnoreabbrev <expr> W getcmdtype() == ":" && getcmdline() == 'W' ? 'w' : 'W'
cnoreabbrev <expr> Q getcmdtype() == ":" && getcmdline() == 'Q' ? 'q' : 'Q'
nnoremap <S-Left>  :tabprevious<CR>
nnoremap <S-Right> :tabnext<CR>
nnoremap gf :vertical wincmd f<CR>
vnoremap gf :vs wincmd f <CR>
noremap <C-e> :!p4 edit %<CR> :e! <CR>
autocmd BufNewFile,BufRead *.e,*.ecom set filetype=specman
autocmd BufNewFile,BufRead *.v,*.vh,*.sv,*.svi,*.svh,*.hdr set filetype=verilog_systemverilog
function MyPythonSettings()    
   setlocal tabstop=4
   setlocal softtabstop=4
   setlocal shiftwidth=4
endfunction
autocmd FileType python call MyPythonSettings()
command DelEmptyLines :%s/\s\+$//e <bar> %s/\n\{3,}/\r\r/e
" GUI Settings
if has("gui_running")      "
   if system("xdpyinfo | grep dimensions | tr -d ' ' | cut -d 'x' -f 2 | cut -d 'p' -f 1") > 900      "
      set guifont=Luxi\ Mono\ 9      "Big Screen
   else     "                              
      set guifont=Luxi\ Mono\ 9      "Small Screen
   endif    "
endif    "
"----------------------------------sv coding shortcuts:---------------------------
nnoremap :<space> :nohlsearch<CR>
nnoremap <C-e> :! sc edit %<CR>  :e! <CR>
map <C-Down> ^i//<Esc>+
imap <C-Down> <Esc>^i//<Esc>+i
map <C-Up> ^i//<Esc>-
imap <C-Up> <Esc>^i//<Esc>-i
:autocmd FileType python map <C-Down> ^i#<Esc>+ //
:autocmd FileType python imap <C-Down> <Esc>^i#<Esc>+i //
:autocmd FileType python map <C-Up> ^i#<Esc>- //
:autocmd FileType python imap <C-Up> <Esc>^i#<Esc>-i //
:autocmd FileType tcsh map <C-Down> ^i#<Esc>+
:autocmd FileType tcsh imap <C-Down> <Esc>^i#<Esc>+i
:autocmd FileType tcsh map <C-Up> ^i#<Esc>-
:autocmd FileType tcsh imap <C-Up> <Esc>^i#<Esc>-i
map ; $i<Right>;
