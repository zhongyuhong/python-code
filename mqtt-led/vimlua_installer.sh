# http://lambdalisue.hatenablog.com/entry/2013/07/03/023934

sudo aptitude install -y libncurses5-dev libgnome2-dev libgnomeui-dev libgtk2.0-dev libatk1.0-dev libbonoboui2-dev liblua5.2-dev libcairo2-dev libx11-dev libxpm-dev libxt-dev python-dev ruby-dev lua5.2 ruby mercurial
sudo aptitude remove vim vim-runtime gvim vim-tiny vim-common vim-gui-common
cd $HOME
mkdir src && cd src
hg clone https://code.google.com/p/vim/
cd vim
./configure --with-features=huge --disable-darwin --disable-selinux --enable-luainterp --enable-perlinterp --enable-pythoninterp --enable-python3interp --enable-tclinterp --enable-rubyinterp --enable-cscope --enable-multibyte --enable-xim --enable-fontset
make
sudo aptitude install -y checkinstall
sudo checkinstall

echo "🍣 vim +lua installation finished 🍣"