""" GNUplot script for plotting several data files into separate images
    Credit goes to Otto Hanski and Weijun Zhou that posted their ideas 
    on stackexchange. I just catered it to plotting supernovae spectra."""

# We start by asking the user what data file extension is used in the folder

print 'Please type the file extension for the script to read (ex: .txt)'
xtn = system('read xtn; echo $xtn')
xtnlen = strlen(xtn)-1

# Then we start the loop, making shure to plot only the files with the correct extension

do for [fn in system("ls")] {
    len=strlen(fn)
    form=substr(fn,len-xtnlen,len)
    if (form eq xtn) {
        set term pngcairo size 900,600 enhanced font 'Vedrana,10'

        data=sprintf("%s",fn)
        filename=sprintf(substr(fn,0,len-xtnlen+1))


        set xlabel 'Wavelenght (Å)'
        set ylabel 'Flux (Lumen)'
        
        set title ''.filename.' spectrum'
        set output ''.filename.'.png'
        plot data using 1:2 with line lc rgb 'red' notitle
        unset output
    }
}
