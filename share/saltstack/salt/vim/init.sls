vim:
  pkg:
    - installed
    - name: vim-enhanced

vimrc:
  file:
    - managed
    - name: ~/.vimrc
    - source: salt://vim/.vimrc
    - mode: 644
