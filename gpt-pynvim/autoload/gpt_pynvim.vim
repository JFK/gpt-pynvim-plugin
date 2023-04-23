if !has("python3")
  echo "vim has to be compiled with +python3 to run this"
  finish
endif
if exists('g:gpt_pynvim_loaded')
    finish
endif

scriptencoding utf-8

let g:gpt_pynvim_loaded = 1
let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '../python'))
sys.path.insert(0, python_root_dir)
import gpt_pynvim
EOF


function! g:gpt_pynvim#GptPyNvim()
let start_time = reltime()
python3 << EOF
gpt_pynvim.main()
EOF
let end_time = reltime()
echo "Loading time: " . reltimestr(reltime(start_time, end_time)) . " seconds"
endfunction

" GPTCommentGenerator Plugin
vnoremap <buffer> , :<C-u>call gpt_pynvim#GptPyNvim()<CR>

" Sample
" command! -nargs=1 GptPyNvim :call gpt_pynvim#GptPyNvim(<f-args>)
