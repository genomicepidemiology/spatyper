#!/usr/bin/gawk -f
# spa_type.find2.gawk
#
# Script that reads in a blast.txt, query.tab (the genome sequence) 
# the blast search is made from the query.tab plus a database made 
# made from all the spa-sequences without 5' and 3' ends
# The 5' and 3' end are matched by this script
# 
# 5': RCAMCAAAA = [GA]CA[AC]CAAAA
# 3': N(18-19)TAYATGTCGT = N(18-19)TA[CT]ATGTCGT


# use: spa_type.find.gawk blast.txt query.tab > res   

BEGIN{
    FS="\t";
    com["A"]="T"; com["T"]="A"; com["G"]="C"; com["C"]="G"; com["N"]="N";
    com["a"]="T"; com["t"]="A"; com["g"]="C"; com["c"]="G"; com["n"]="N";
    dir["A"]="A"; dir["T"]="T"; dir["G"]="G"; dir["C"]="C"; dir["N"]="N";
    dir["a"]="A"; dir["t"]="T"; dir["g"]="G"; dir["c"]="C"; dir["n"]="N";
    nb=0;
}
{
    if(FILENAME==ARGV[1]){
	nb++;
        split($2,a," ");
        qname[nb] = a[1];
        qnum[a[1]] = nb;
        split($1,a," ");
        split(a[1],a1,"_");
        bname[nb] = a1[1] "_" a1[2];
        orien[nb] = "plus";
        if($9>$10) orien[nb] = "minus";
        qpos1[nb]=$9;
        qpos2[nb]=$10;
    }
    if(FILENAME==ARGV[2]){
	split($1,a," ");
	if(a[1] in qnum) qseq[a[1]] = $2;
    }
}
END{
    for(i=1;i<=nb;i++){
	if(orien[i]=="plus"){
            pos1[i] = qpos1[i]-9;
            pos2[i] = qpos2[i]+29;
	    seq = substr(qseq[qname[i]],qpos2[i]+19,11); # 5' sequence
            end5seq[i] = "";
            for(j=1;j<=length(seq);j++) end5seq[i] = end5seq[i] dir[substr(seq,j,1)];
	    seq = substr(qseq[qname[i]],qpos1[i]-9,9); # 3' sequence
            end3seq[i] = "";
            for(j=1;j<=length(seq);j++) end3seq[i] = end3seq[i] dir[substr(seq,j,1)];
        }
	if(orien[i]=="minus"){
            pos1[i] = qpos2[i]-29;
            pos2[i] = qpos1[i]+9;
	    seq = substr(qseq[qname[i]],qpos2[i]-29,11); # 5' sequence
            end5seq[i] = "";
            for(j=1;j<=length(seq);j++) end5seq[i] = com[substr(seq,j,1)] end5seq[i];
	    seq = substr(qseq[qname[i]],qpos1[i]+1,9); # 3' sequenceCA[AC]CAAAA
            end3seq[i] = "";
            for(j=1;j<=length(seq);j++) end3seq[i] = com[substr(seq,j,1)] end3seq[i];
        }
        if(end5seq[i] ~ "TA[CT]ATGTCGT" && end3seq[i] ~ "[GA]CA[AC]CAAAA")printf("Bingo\t%s\t%s\tposition:%d-%d\t%s\n",bname[i],qname[i],pos1[i],pos2[i],orien[i]);
	#else{ # write out if only 5' or 3' end matches
	    #if(end5seq[i] ~ "TA[CT]ATGTCGT")printf("5'ingo\t%s\t%s\tposition:%d-%d\t%s\n",bname[i],qname[i],pos1[i],pos2[i],orien[i]);
	    #if(end3seq[i] ~ "[GA]CA[AC]CAAAA")printf("3'ingo\t%s\t%s\tposition:%d-%d\t%s\n",bname[i],qname[i],pos1[i],pos2[i],orien[i]);
	#}
    }
}
