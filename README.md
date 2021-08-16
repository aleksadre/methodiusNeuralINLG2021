# A repo for the paper "Neural Methodius Revisited: Do Discourse Relations Help with Pre-Trained Models Too?"
by Aleksandre Maskharashvili, Symon Stevens-Guille, Xintong Li and Michael White

## Corpus
The corpus is in the folder 'corpus'. There are several files:

- train_without_few.tsv  --- this is the file used for training zero shot models 
- 10UnlikeLike.tsv  --- it contains 10 examples starting with Unlike and 10 examples starting with Like which we use for 10-shot learning
- few.tsv        --- it contains        3 examples starting with Unlike and 3 examples starting with Like which we use for 10-shot learning
- valid.tsv         ---  is the  validation file
- test.tsv           ---     Standard test file
- 237test.mr-ar.tsv   ---    Challenge test file


To produce text versions of these files, you can use our script 'textVesions.py' from the 'corpus_scripts' folder as follows: 
```
	python textVesions.py inputfile outpufile
```
where inputfile is one of the above listed names; outpufile is the name of the produced file. 

To generate corpora of various size (1, 3, 5, 10, 20 and 50 percent of the data) as we do in our experiments, you can use our scripts from 'corpus_scripts' as follows:

- copy files from the 'corpus_scripts' foder into the 'corpus' folder
- run the command: 
```
      perc_script.sh argument
```
where argument is either: 'few' or '10UnlikeLike'. If no argument is provided, then it will create zero-shot corpora. This will create a folder 'subsets_Text_and_Structure_argument' (in case of no argument, it will create the subsets_Text_and_Structure_zshot folder) containing various sub-folders corresponding to 1, 3, 5, 10, 20, and 50 percent of data for RSTstruct, FACTstruct, RSTText, and FactText models. Each of them is created in 5 versions. All of them contain a file 'indivisible_tokens.txt.'

To use 100% of data for the models RSTstruct, FACTstruct, RSTText, and FactText, one can use the script:
```
      100per_script.sh argument
```
where argument is either: 'few' or '10UnlikeLike' or empty. It the RSTstruct, FACTstruct, RSTText, and FactText data in the folder '100subsets_Text_and_Structure_argument,' each in three copy (shuffled). 


## Installing T-5 and fine-tuning

We use T-5 from [huggingface](https://github.com/huggingface/transformers). For installing the versions of T-5 of [huggingface](https://github.com/huggingface/transformers) and the respective codes that we use, please visit [Leveraging Large Pretrained Models for WebNLG 2020](https://github.com/znculee/webnlg2020).
You can put in data-prep folder your folder containing train.mr, train.lx, valid.mr, valid.lx, test.mr, test.lx, 237test.mr-ar.mr, 237test.mr-ar.lx, and inivisible_tokens.txt files (which you can generate by the above scripts).

If you follow installation of [Leveraging Large Pretrained Models for WebNLG 2020](https://github.com/znculee/webnlg2020), we provide our scripts for training and generating in the folder 'tg_scripts'. You can put them in the 'scripts' folder. To train and generate, you can use:

```
bash scripts/methodius_train.t5_large.sh yourcoprusname
bash scripts/methodius_generate.t5_large.sh yourcoprusname test
bash scripts/methodius_generate.t5_large.sh yourcoprusname 237test.mr-ar
```

Where 'yourcoprusname' is a directory in 'data-prep' folder with the relevant data.



## Evaluations

After generating output realizations for test.mr and 237test.mr-ar.mr, one can calculate number of various kinds of errors. In the directory with 'hyp.test.txt' and 'hyp.237test.mr-ar.txt' (corresponding to the generated files for 'test' and '237test.mr-ar' test files), put the following files: 'test.mr', 'test.lx', '237test.mr-ar.mr', '237test.mr-ar.lx', and also the files from the directroy 'evaluation_scripts'. 
To obtain results about repetitions, hallucinations and ommisiosn (RHO errors) and number of errors in discourse relation realization, you can run the following command:
```
	bash scr_compareGen.sh
```
It produces files with the following names:
```
	- RHO_deinfl_gen.t5hugface.test.txt
	- numRelCount_deinfl_gen.t5hugface.test.txt
	- RHO_deinfl_gen.t5hugface.237test.mr-ar.txt
	- numRelCount_deinfl_gen.t5hugface.237test.mr-ar.txt
```

To calculate so-called mistaken identity errors, you can put test.tsv and '237test.mr-ar.tsv' in the same folder as 'hyp.test.mr-ar.txt' and 'hyp.237test.mr-ar.txt' and run the scripts:
```
- python mistID_errors.py 1 
- python mistID_errors.py
```
They will find mistaken identity errors for test files 'hyp.test.txt'  and 'hyp.237test.mr-ar.txt' respectively. 


They will find mis identity errors for test files 'hyp.test.txt'  and 'hyp.237test.mr-ar.txt' respectively. 

## Statistical Significance

In folder 'stat_sign', we have scripts for statistical significance, which we calculate using stratified approximated  randomization. The script file is 'stratAR.py.' There is a sub-folder 'stat_sign_demo' demo with files that you can run as follows:
```
python sAR_comp.py
```
