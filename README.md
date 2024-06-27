# DataPipeline
Starter template for data pipelines 

So you want to make a data pipeline, eh? To do this, follow these steps.
1. In a terminal, navigate to the directory you would like to create the pipeline in. Then run:

    $ git clone https://github.com/EcotopeResearch/starter_pipeline.git
    
This will copy this template into the directory. By default, it will call this template "starter_pipeline", so go ahead and rename this folder something more useful, like the name of the site the data will be processed for. For simplicity, I will be refering to this directory as "starter_pipeline", just know to replace that in the following steps with whatever you choose to name your data pipeline directory.

2. Work with your IT department to make sure data for the site will land in starter_pipeline/data/

3. Fill out your database credentials specify the tables you would like to push data to in starter_pipeline/code/Pipeline/src/config.ini and save the file.

4. Open starter_pipeline/code/Pipeline/src/extract.py and delete the appropriate block of code to reflect the type of data you will be recieving

5. Once data from the site is landing in starter_pipeline/data/, follow these steps to configure what data will end up in your database table:
   
        1. In a terminal, navigate to starter_pipeline/code/helpful_scripts/
        2. Edit create_full_var_names.py in the top section to set file_suffix = '.gz', or '.csv' if data is in Modbus format,  and then set Run the command 
            $ python create_full_var_names.py
            This will create a file called variable_names_full.csv under starter_pipeline/input/ that contains all the varriables.
        3. Fill out the columns (particularly the variable_name column) for each variable you would like to end up in the database. NOTE: make sure you do not include any spaces or commas in the varriable_names column.
            Work with the project’s design engineer to name points and follow Ecotope’s variable naming conventions:
            i.	Names should be VariableType_EquipmentName (ex. Flow_HPWH1, PowerIn_SwingTank)
            ii.	Temperature variables should start with ‘Temp_’
            iii.	Power variables should start with ‘PowerIn_’
            iv.	Flow variables should start with ‘Flow_’
            v.	Calculated heat variables should start with ‘HeatOut_’
        4. In a terminal, navigate to starter_pipeline/code/helpful_scripts/ and run 
            $ python compress_full_varriable_names.py
        This will create a compressed Variable_Names.csv under starter_pipeline/input/
        
6. Since this is just a starter template, you will likely need to make some modifications and customizations to how you process data by editing the contents of pipeline.py, extract.py, transform.py, and/or load.py, all under starter_pipeline/code/Pipeline. Steps for running and testing your code locally can be found below 

To run and test your pipeline code, first set up your anaconda environment from the anaconda prompt
1. Navigate to your MariaPipeline directory
2. Run the following command 

    $ conda env create --file dataPipeline.yml

3. Activate the created environment

    $ conda activate dataPipeline

To run the pipeline from your Pipeline directory

    $ python src\pipeline.py

Once your code is working the way you want it, consider setting up a cron job to automatically run your code on a regular basis to update your database with fresh data.

-----------------------------------------------------------------------------
------------------THIS NEXT SECTION APPLIES TO ECOTOPE ONLY------------------
-----------------------------------------------------------------------------

Once the pipeline has been set up to satisfaction, please fill out a new row for the site in the variable_names_locations.csv in the \cron_jobs sub directory 
of the dash app directory. Then run the population script there
    
    $ python populate_config.py

