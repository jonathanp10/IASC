--------------------------------- code starts here ----------------------------
" Modeline and Notes
"   This is my personal .vimrc, I don't recommend you copy it, just
"   use the "   pieces you want(and understand!).  When you copy a
"   .vimrc in its entirety, weird and unexpected things can happen.
"
echo &filetype
" Startup
   set tabpagemax=100      " change tab-limit
   set guitablabel=%t\%M   " Short tab label

   set nocompatible        " no need to be compatible with VI
   set modelines=0         " Prevents security exploits that may be done when modelines is used

" Basics
   colorscheme desert      " awesome colorscheme
   syntax on               " syntax highlighted on
   syntax enable           " enable syntax processing
   filetype indent on
   set wrap
   set lbr


   set tabstop=3           " number of visual spaces per TAB
   set softtabstop=3       " number of spaces in tab when editing
   set shiftwidth=3        " number of spaces for each step of autoident 
   set expandtab           " tabs are spaces

" UI config
   set number              " show line numbers
   set showcmd             " show command in bottom bar
   set ch=2                " Make command line two lines high
   set cursorline
   set nowrap              " do not wrap single lines into multiple ones
   set textwidth=0         " avoid automatic word wrapping, nowrap was not enough

   set ignorecase          " case insensitive search (default is case sensitive)
   set smartcase           " search is case-sensitive if an uppercase if the search pattern contains an uppercase letter 
   set hlsearch            " highlight search matches
   set incsearch           " searches from the first input and refines search as you write more letters

   set wrapscan            " This is the default option, search wraps at the bottom
   set wildmenu
   set wildignore=*.dll,*.o,*.obj,*.bak,*.exe,*.pyc,*.jpg,*.gif,*.png
   set wildmode=list:longest " turn on wild mode huge list

" Backups
   set backup
   set backupdir=~/.vim/backup  " directory for ~backup files 
   set directory=~/.vim/tmp     " directory for swp files

" NEW Additions tentative add
   set showmatch
   set matchtime=5
   set autoindent cindent        " Abbreviations work with this settings 
   set clipboard+=noautoselect
   "set clipboard+=unnamed
   set clipboard+=unnamedplus
   set autochdir




 nnoremap <C-a> [[v<S-g>         
   inoremap <C-a> <Esc>[[v<S-g>

   nnoremap <C-s> :w<CR>
   inoremap <C-s> <ESC>:w<CR><Ins>

   nnoremap <C-z> u
   inoremap <C-z> <Esc>u<Ins>
       
   vnoremap <C-x> "+x      
   vnoremap <C-c> "+y
   "nnoremap <C-v> "+P   used for entering visual mode (do twice in order to paste)
   "inoremap <C-v> <Esc>"+P
   "vnoremap <C-v> "+P

   "Maps CMD-V to Ctrl-V (Enter Visual Block Mode)
   "nnoremap <M-v> <C-v>8h             

   "Maps :X -> :x, :Q->:q, :W->:w, in case of caps lock or accidental shift holding" 
   cnoreabbrev <expr> X getcmdtype() == ":" && getcmdline() == 'X' ? 'x' : 'X'
   cnoreabbrev <expr> W getcmdtype() == ":" && getcmdline() == 'W' ? 'w' : 'W'
   cnoreabbrev <expr> Q getcmdtype() == ":" && getcmdline() == 'Q' ? 'q' : 'Q'

   " Tab navigation (like unix shell) 
   nnoremap <S-Left>  :tabprevious<CR>
   nnoremap <S-Right> :tabnext<CR>

   " Move tabs around
   nnoremap <silent> <S-C-Left>  :execute 'silent! tabmove ' . (tabpagenr()-2)<CR>
   nnoremap <silent> <S-C-Right> :execute 'silent! tabmove ' . tabpagenr()<CR>

   " get-file now opens a new tab rather than linking in the same tab
   "nnoremap gf <C-W>gf
   "vnoremap gf <C-W>gf
   nnoremap gf :vertical wincmd f<CR>
   vnoremap gf :vs wincmd f <CR>

   noremap <C-e> :!p4 edit %<CR> :e! <CR>


   " maximize window
   "nnoremap <C-m> :set lines=999 columns=999 <CR>


" FileSpecific
autocmd BufNewFile,BufRead *.e,*.ecom set filetype=specman
autocmd BufNewFile,BufRead *.v,*.vh,*.sv,*.svi,*.svh,*.hdr set filetype=verilog_systemverilog

function MyPythonSettings()
   setlocal tabstop=4
   setlocal softtabstop=4
   setlocal shiftwidth=4
endfunction
autocmd FileType python call MyPythonSettings()

function MyPerlSettings()
   setlocal tabstop=4
   setlocal softtabstop=4
   setlocal shiftwidth=4
endfunction
autocmd FileType perl call MyPerlSettings()

function MySystemVerilogSettings()
   "setlocal tabstop=4
   "setlocal softtabstop=4
   "setlocal shiftwidth=4

   ab qfatal `uvm_fatal("RANPRINT", $sformatf("This is a FATAL assert"))
   ab qmessage `uvm_info("RANPRINT", $sformatf("RANPRINT_num00"), UVM_LOW)
   ab qcase case (aru_signal) <CR>value1 : action1;<CR>value2 : action2;<CR>default : `uvm_fatal("QCASE", $sformatf("Default: This is a FATAL assert"))<CR>endcase
   ab qfor for (int idx = 0 ; idx < 10 ; idx++) begin<CR>`uvm_info("CPU_Driver", $sformatf("INDEX: %d", idx), UVM_LOW)<CR>end
   ab qforeach foreach (any_array[idx]) begin<CR>`uvm_info("CPU_Driver", $sformatf("INDEX: %d", idx), UVM_LOW)<CR>end
   ab qfork fork<CR>begin<CR>end<CR>begin<CR>end<CR>join<CR>disable fork;<CR>
   ab qcomment // =============================================================================<CR>// Title <CR>// =============================================================================<CR>
   ab qcomment2 <TAB>// ==========================================================================<CR>// Title <CR>// ==========================================================================<CR>
endfunction
autocmd FileType verilog_systemverilog call MySystemVerilogSettings()

function MySpecmanSettings()
   " q - quick
   ab qmessage message(LOW, "[RANPRINT - This is a quickmessage]", some_var);
   ab qassert  assert(must_be_true_expr) else error("Expression Was False");
   ab qfor     for idx from 1 to 10 { <CR>out(idx);<CR>}; 
   ab qforeach for each (datum) in data { <CR>out("index", index, "datum", datum);<CR>};
   ab qfirstof first of <CR>{<CR>{<CR>};<CR>{<CR>};<CR><BS>};
   ab qallof   all of <CR>{<CR>{<CR>};<CR>{<CR>};<CR><BS>};
   ab qcase    case (aru_signal) { <CR>value1 : { action1; }; <CR>value2 : { action2; }; <CR>};
endfunction
autocmd FileType specman call MySpecmanSettings()

autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o

" myCommads
command DelEmptyLines :%s/\s\+$//e <bar> %s/\n\{3,}/\r\r/e
command CheatUVM :vs ~rannis/personal/history/history_uvm.sv
command CheatSpecman :vs ~rannis/personal/history/history_specman.e

" GUI Settings
if has("gui_running")
   if system("xdpyinfo | grep dimensions | tr -d ' ' | cut -d 'x' -f 2 | cut -d 'p' -f 1") > 900
      set guifont=Luxi\ Mono\ 9      "Big Screen
   else                              
      set guifont=Luxi\ Mono\ 9      "Small Screen
   endif
endif



----------------------------------sv coding shortcuts:---------------------------
nnoremap :<space> :nohlsearch<CR>
nnoremap <C-e> :! sc edit %<CR>  :e! <CR>
inoremap uvminfo<C-space> `uvm_info("string_id", "string message", UVM_LOW)  
inoremap uvmerror<C-space> `uvm_error(string_id, "string message")  
inoremap uvmfatal<C-space> `uvm_fatal(string_id, "string message") 


" smart begin
inoremap begin<C-space> begin<Enter>end<Enter> 

inoremap _uvmcreate<space><space> type::type_id::create("instance name",this); 


" smart comment:
map <C-Down> ^i//<Esc>+
imap <C-Down> <Esc>^i//<Esc>+i
map <C-Up> ^i//<Esc>-
imap <C-Up> <Esc>^i//<Esc>-i
map <C-S-Down> ^xx+
imap <C-S-Down> <Esc>^xx+i
map <C-S-Up> ^xx<Esc>-
imap <C-S-Up> <Esc>^xx<Esc>-i

" comment for python:
:autocmd FileType python map <C-Down> ^i#<Esc>+
:autocmd FileType python imap <C-Down> <Esc>^i#<Esc>+i
:autocmd FileType python map <C-Up> ^i#<Esc>-
:autocmd FileType python imap <C-Up> <Esc>^i#<Esc>-i
:autocmd FileType python map <C-S-Down> ^x+
:autocmd FileType python imap <C-S-Down> <Esc>^x+i
:autocmd FileType python map <C-S-Up> ^x<Esc>-
:autocmd FileType python imap <C-S-Up> <Esc>^x<Esc>-i

" comment for tcsh:
:autocmd FileType tcsh map <C-Down> ^i#<Esc>+
:autocmd FileType tcsh imap <C-Down> <Esc>^i#<Esc>+i
:autocmd FileType tcsh map <C-Up> ^i#<Esc>-
:autocmd FileType tcsh imap <C-Up> <Esc>^i#<Esc>-i
:autocmd FileType tcsh map <C-S-Down> ^x+
:autocmd FileType tcsh imap <C-S-Down> <Esc>^x+i
:autocmd FileType tcsh map <C-S-Up> ^x<Esc>-
:autocmd FileType tcsh imap <C-S-Up> <Esc>^x<Esc>-i

// add ; in n-mode
map ; $i<Right>;
--------------------------------- code ends  here ----------------------------
