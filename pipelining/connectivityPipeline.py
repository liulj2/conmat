#!/usr/bin/env python

import os
import glob
import shutil
import sys

#--------------------------------------------------------------------------------

# # enter project directory
# projectName = sys.argv[1]
# projectPath = '/archive/data-2.0/' + projectName + '/data/nii/'

# os.chdir(projectPath)

# projectSubjects = glob.glob('*')
# projectSubjects.sort()

# # for all the projects which have nii pipeline folders
# for subjectID in projectSubjects:
# 	if "PHA" not in subjectID:
# 		print(subjectID)
# 		# check for bedpostx pipeline and conmat do not exist already?

projectName = sys.argv[1]
subjectID = sys.argv[2]

bedpostXPipeDir = '/scratch/lliu/' + projectName + '/pipelines/bedpostX/' + subjectID + '/'
conmatPipeDir = '/scratch/lliu/' + projectName + '/pipelines/conmat/' + subjectID + '/'
dtiPipeDir = '/archive/data-2.0/' + projectName + '/pipelines/dtifit/' + subjectID + '/'
hcpPipeDir = '/archive/data-2.0/' + projectName + '/pipelines/hcp/' + subjectID + '/T1w/'

mniAtlasDir = '/projects/lliu/ImportantFiles/'
tempSubjDir = '/scratch/lliu/tmp/' + subjectID + '/'
tempSubjName = '/scratch/lliu/tmp/' + subjectID
eyeFile = tempSubjName + '.bedpostX/xfms/eye.mat'
conmatPipeDir = '/scratch/lliu/' + projectName + '/pipelines/conmat/' + subjectID + '/' 

def main():
	# flag = 0
	# while flag != 1:
	# 	if os.path.exists(dtiPipeDir):
	# 		if not os.path.exists(tempSubjDir):
	# 			getFiles()
	# 			if os.path.exists(bedpostXPipeDir) and not os.path.exists(tempSubjName + '.bedpostX'):
	# 				getBedpostX()
	# 			elif not os.path.exists(bedpostXPipeDir) and not os.path.exists(tempSubjName + '.bedpostX'):
	# 				runBedpostX()
	# 			else:
	# 				copyBedpostX()
	# 		elif not os.path.exists(conmatPipeDir) and os.path.exists(eyeFile):
	# 			register()
	# 			runConmat()
	# 			getFaMat('mean')
	# 			getMdMat('mean')
	# 			# removeTempFiles()
	# 			flag = 1
	# 		else:
	# 			flag = 0
	# 	else:
	# 		flag = 1
	if os.path.exists(dtiPipeDir):
		if os.path.exists(tempSubjDir):
			flag = 0
			while flag != 1:
				if os.path.exists(tempSubjName + '.bedpostX'):
					if os.path.exists(bedpostXPipeDir):
						flag = 1
					elif os.path.exists(eyeFile):
						copyBedpostX()
						flag = 1
					else:
						flag = 0
				else:
					if os.path.exists(bedpostXPipeDir):
						getBedpostX()
						flag = 1
					else:
						runBedpostX()
						flag = 0
			flag = 0
			while flag != 1:
				if os.path.exists(conmatPipeDir):
					flag = 1
				else:
					register()
					runConmat()
					getFaMat('max')
					getFaMat('mean')
					getFaMat('min')
					getMdMat('max')
					getMdMat('mean')
					getMdMat('min')
					flag = 1
			# flag = 0
			#while flag != 1
				# check if bedpostx file is in temp
					#if it is, check if the eye file is there
						# if it is, do nothing, flag = 1
						# if it's not, flag = 0
					#if it's not, check if it's in the pipeline
						#if it is, copy it over to temp, flag = 1
						# if it's not, run bedpostx, flag = 0
			#flag = 0
			#while flag != 1
				# check if conmat folder exists
					# if it does, flag = 0
					# if it doesnt, register and run conmat, flag = 1
		# if temp does not exist, get files
		else: 
			getFiles()

		# 		getFiles()
		# 		if os.path.exists(bedpostXPipeDir) and not os.path.exists(tempSubjName + '.bedpostX'):
		# 			getBedpostX()
		# 		elif not os.path.exists(bedpostXPipeDir) and not os.path.exists(tempSubjName + '.bedpostX'):
		# 			runBedpostX()
		# 		else:
		# 			copyBedpostX()
		# 	elif not os.path.exists(conmatPipeDir) and os.path.exists(eyeFile):
		# 		register()
		# 		runConmat()
		# 		getFaMat('mean')
		# 		getMdMat('mean')
		# 		# removeTempFiles()
		# 		flag = 1
		# 	else:
		# 		flag = 0
		# else:
		# 	flag = 1


#--------------------------------------------------------------------------------

def getFiles():
	os.chdir(dtiPipeDir)
	if glob.glob('*_eddy_correct.nii.gz') != []:
		shutil.copytree(dtiPipeDir, tempSubjDir)
		shutil.copy(hcpPipeDir + 'wmparc.nii.gz', tempSubjDir)
		shutil.copy(hcpPipeDir + 'T1w_brain.nii.gz', tempSubjDir)
		shutil.copy(mniAtlasDir + 'shen_2mm_268_parcellation.nii.gz', tempSubjDir)
		shutil.copy(mniAtlasDir + 'MNI152_T1_2mm_brain.nii.gz', tempSubjDir)

		os.chdir(tempSubjDir)

		shutil.copyfile(tempSubjDir + glob.glob('*.bval')[0], tempSubjDir + 'bvals')
		shutil.copyfile(tempSubjDir + glob.glob('*.bvec')[0], tempSubjDir + 'bvecs')
		shutil.copyfile(tempSubjDir + glob.glob('*_eddy_correct_b0_bet_mask.nii.gz')[0], tempSubjDir + 'nodif_brain_mask.nii.gz')
		shutil.copyfile(tempSubjDir + glob.glob('*_eddy_correct.nii.gz')[0], tempSubjDir + 'data.nii.gz')
	else:
		return

def getBedpostX():
	shutil.copytree(bedpostXPipeDir + subjectID + '.bedpostX', tempSubjName + '.bedpostX')

def runBedpostX():
	os.chdir(tempSubjDir)

	os.system('bedpostx ./')

def copyBedpostX():
	# flag = 0
	# while flag != 1:
	# 	if os.path.exists(eyeFile):
	shutil.copytree(tempSubjName + '.bedpostX', bedpostXPipeDir + subjectID + '.bedpostX')
			# flag = 1

def register():
	os.chdir(tempSubjDir)

	b0Mask = glob.glob('*_b0_bet_mask.nii.gz')[0] 
	b0Brain = glob.glob('*_b0_bet.nii.gz')[0] 
	multiVol = glob.glob('*_eddy_correct.nii.gz')[0]
	T1wBrain = 'T1w_brain.nii.gz' 
	wmParc = 'wmparc.nii.gz' 
	mniBrain = 'MNI152_T1_2mm_brain.nii.gz' 
	shenParc = 'shen_2mm_268_parcellation.nii.gz' 
	bvecFile = '*.bvec'
	bvalFile = '*.bval'

	os.system('echo "making scheme file"')
	os.system('fsl2scheme \
		-bvecfile ' + bvecFile + ' \
		-bvalfile ' + bvalFile + ' > bVectorScheme.scheme')

	os.system('echo "registering b0-T1"')
	os.system('flirt \
		-in ' + b0Brain + ' \
		-ref ' + T1wBrain + ' \
		-omat tfm.mat')

	os.system('convert_xfm \
		-omat tfm_invert.mat \
		-inverse tfm.mat')

	os.system('echo "registering white matter mask"')
	os.system('flirt \
		-in ' + wmParc + ' \
		-ref ' + b0Brain + ' \
		-applyxfm \
		-init tfm_invert.mat \
		-o wmparc_invert.nii.gz')

	os.system('fslmaths \
		wmparc_invert.nii.gz \
		-thr 2500 \
		-bin wmparc_invert_bin.nii.gz')

	os.system('echo "registering MNI"')
	os.system('flirt \
		-in ' + mniBrain + ' \
		-ref ' + b0Brain + ' \
		-interp nearestneighbour \
		-omat mni.mat')

	os.system('echo "registering atlas"')
	os.system('flirt \
		-in ' + shenParc + ' \
		-ref ' + b0Brain + ' \
		-interp nearestneighbour \
		-applyxfm \
		-init mni.mat \
		-o atlas.nii.gz')

	os.system('echo "fitting tensors"')
	os.system('wdtfit ' + multiVol + ' \
		bVectorScheme.scheme \
		-brainmask ' + b0Mask + ' \
		-outputfile wdt.nii.gz')

def runConmat():
	os.chdir(tempSubjDir)

	os.system('echo "streamlining"')
	os.system('track \
		-bedpostxdir ' + tempSubjName + '.bedpostX' + ' \
		-inputmodel bedpostx_dyad \
		-seedfile wmparc_invert_bin.nii.gz \
		-curvethresh 90 \
		-curveinterval 2.5 \
		-anisthresh 0.2 \
		-tracker rk4 \
		-interpolator linear \
		-iterations 1 \
		-brainmask nodif_brain_mask.nii.gz | procstreamlines \
		-endpointfile atlas.nii.gz \
		-outputfile bedDetTracts.Bfloat')

	os.system('echo "calculating connectivity matrix"')
	os.system('conmat \
		-inputfile bedDetTracts.Bfloat \
		-targetfile atlas.nii.gz \
		-tractstat length \
		-outputroot ' + subjectID + '_bedpostX_det_')

	os.makedirs(conmatPipeDir)
	shutil.copyfile(tempSubjDir + glob.glob('bedDetTracts.Bfloat')[0], conmatPipeDir + subjectID + '_detTracts.Bfloat')
	shutil.copyfile(tempSubjDir + glob.glob('*.scheme')[0], conmatPipeDir + subjectID + '.scheme')
	shutil.copyfile(tempSubjDir + glob.glob('wdt.nii.gz')[0], conmatPipeDir + subjectID + '_wdtfit.nii.gz')
	shutil.copyfile(tempSubjDir + glob.glob('atlas.nii.gz')[0], conmatPipeDir + subjectID + '_registered_shen.nii.gz')
	shutil.copyfile(tempSubjDir + glob.glob('*_sc.csv')[0], conmatPipeDir + subjectID + '_bedpostX_det_connectivity.csv')
	shutil.copyfile(tempSubjDir + glob.glob('*_ts.csv')[0], conmatPipeDir + subjectID + '_bedpostX_det_length.csv')

def getFaMat(stat):
	os.chdir(tempSubjDir)
	os.system('fa -inputfile wdt.nii.gz -outputfile fa.nii.gz')

	os.system('echo "calculating connectivity matrix"')
	os.system('conmat \
		-inputfile bedDetTracts.Bfloat \
		-targetfile atlas.nii.gz \
		-scalarfile fa.nii.gz \
		-tractstat ' + stat + ' \
		-outputroot ' + subjectID + '_fa_' + stat + '_')

	shutil.copyfile(tempSubjDir + glob.glob('*_ts.csv')[0], conmatPipeDir + subjectID + '_bedpostX_det_fa_' + stat + '.csv')

def getMdMat(stat):
	os.chdir(tempSubjDir)
	os.system('md -inputfile wdt.nii.gz -outputfile md.nii.gz')

	os.system('echo "calculating connectivity matrix"')
	os.system('conmat \
		-inputfile bedDetTracts.Bfloat \
		-targetfile atlas.nii.gz \
		-scalarfile md.nii.gz \
		-tractstat ' + stat + ' \
		-outputroot ' + subjectID + '_md_' + stat + '_')

	shutil.copyfile(tempSubjDir + glob.glob('*_ts.csv')[0], conmatPipeDir + subjectID + '_bedpostX_det_md_' + stat + '.csv')

def removeTempFiles():
	shutil.rmtree(tempSubjDir)
	shutil.rmtree(tempSubjName + '.bedpostX')

#--------------------------------------------------------------------------------

if __name__ == '__main__':
	main()