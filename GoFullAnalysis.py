import os
import sys
import Config
from datetime import datetime
from time import sleep
def usage():
	print """ This is the wrapper to get the GO distribution from a BLAST result
	goFullAnalisis.py in_file.fasta wanted_gos1,wanted_gos2 out_dir refseq|uniprot
	"""
	exit()
#	GoDistribution.py contigs2go.csv GOswanted Counted_GOs.tab go2contigs.csv
# 	hits2go.py querys2hits.csv hits2terms.csv

def td2seconds(td):
	seconds=(td.days*1440*60)+td.seconds
	return seconds

def main():
	if len(sys.argv)!=5:
		usage()
	in_file=sys.argv[1]
	out_dir=sys.argv[3]
	gos_buscados=sys.argv[2].split(",")
	db_blast=sys.argv[4]
	if db_blast=="refseq":
		db_blast=Config.nrdb
	elif db_blast=="uniprot":
		db_blast=Config.updb
	else:
		usage()
	hit2terms_file="%s/hits2terms.csv" % out_dir
	counted_GOs="%s/Counted_GOs.tab" % out_dir
	go2contigs_file="%s/go2contigs.csv" % out_dir
	out_img="%s/output.png" % out_dir
	out_pdf="%s/Report.pdf" % out_dir
	salida_csv='%s/query2hits.csv' % out_dir
	salida_xml='%s/query2hits.xml' % out_dir
	archivo_entrada=salida_csv
	print "The output dir is: %s" % out_dir
	print "The  XML output of blast will be on %s" % salida_xml
	print "The  CSV output of blast will be on %s" % salida_csv
	print "The GO terms wanted are in: %s" % gos_buscados
	print "The input file is: %s" % archivo_entrada
	print "The file containing relation bettwen sequences and terms is: %s" % hit2terms_file
	print "The GO terms to Sequences file is: %s" % go2contigs_file
	print "The count file of wanted GO terms is: %s" % counted_GOs
	print "The pie char will be generated to: %s" % out_img
	print "The PDF report will be generated on: %s" % out_pdf
	print "*************************Running process******************"
	print "Creating output directory..."
	mkdir_c=os.system('mkdir %s' % out_dir)
	print "Executing BLAST"
	ti=datetime.now()
	blast_c=os.system('python BlastExec.py %s %s %s' % (in_file, db_blast, salida_xml))
	blast_time=datetime.now()-ti
	print "Getting top hits and writing csv file"
	ti=datetime.now()
	convert_c=os.system("python Utilities/BlastXML2CSVCustom.py %s %s" % (salida_xml, salida_csv ))
	convert_time=datetime.now()-ti
	print "Doing associations bettwen hits and gos...."
	ti=datetime.now()
	hit2go_c=os.system("python Hits2Go.py"+" "+archivo_entrada+" "+hit2terms_file)
	h2g_time=datetime.now()-ti
	print "Blast execution time: %s , Used database: %s" % (str(td2seconds(blast_time)), sys.argv[4])
	print "Best hit execution time: %s" % (str(td2seconds(convert_time)))
	print "Hits 2 GO execution time: %s" % (str(td2seconds(h2g_time)))
	print "Generating distributions......"
	for go_buscado in gos_buscados:
	    go_in = go_buscado[::-1].split("/")[0][::-1]
 	    counted_GOs="%s/Counted_%s.tab" % (out_dir,go_in)
            go2contigs_file="%s/%s_2_contigs.csv" % (out_dir, go_in)
            out_img="%s/Pie_%s.png" % (out_dir, go_in)
            out_pdf="%s/Report_%s.pdf" % (out_dir, go_in)
	    ti=datetime.now()
	    print "Generating for %s" % (go_in)
	    goDis_c=os.system("python2 GoDistribution.py"+ " "+ hit2terms_file+" "+go_buscado+" "+counted_GOs+" "+go2contigs_file)
      	    goDis_time=datetime.now()-ti
            print "Go Distribution executing time for %s was %s seconds" % (go_in, str(td2seconds(h2g_time)))
	    print "Generating Pie Char"
	    charPie=os.system("python2 Utilities/GraphPie.py "+ counted_GOs +" "+ out_img)
	    print "Generating PDF report"
 	    try:
		genPDF=os.system("python2  Utilities/PdfGen.py "+ counted_GOs +" "+ out_pdf+" "+out_img)
	    except:
		print "Unable to create PDF report"

	#print "Term distribution execution time %s" % (str(td2seconds(goDis_time))) 
	"""print "Blast execution time: %s , Used database: %s" % (str(blast_time), sys.argv[4])
	print "Best hit execution time: %s" % (str(convert_time))
	print "Hits 2 GO execution time: %s" % (str(h2g_time))
	print "Term distribution execution time %s" % (str(goDis_time))""" 

main()


def timedelta2seconds(cadena):
	dias=cadena.split("day")[0].split(" ")[-2]
	numeros=cadena.split("day")[1].replace(",","").replace(" ","")
	horas=numeros.split(":")[0]
	minutos=numeros.split(":")[1]
	segundos=numeros.split(":")[2].split(".")[0]
	print dias +" "+  horas+ " "+ minutos +" "+ segundos
	t=timedelta(days=int(dias), minutes=int(minutos), seconds=int(segundos), hours=int(horas))
	print t
	print -(t.total_seconds())

	

	

