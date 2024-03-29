# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/04_evaluation.causal.ipynb (unless otherwise specified).

__all__ = ['DEFAULT_LOGGING', 'MethodName', 'TargetUnit', 'RefuteEstimate', 'PropensityWeighting', 'CausalCodeGen',
           'CausalCodeGenNoGraph', 'CausalCodeGenIV', 'CausalCodeGenMultiple']

# Cell
import numpy as np
import pandas as pd

import dowhy
from dowhy import CausalModel
import dowhy.datasets

# Cell
from enum import Enum, auto
from abc import ABC,abstractmethod
import logging

# Cell
# Avoid printing dataconversion warnings from sklearn
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)

# Cell
#export
import logging.config
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        '': {
            'level': 'WARN',
        },
    }
}

logging.config.dictConfig(DEFAULT_LOGGING)

# Cell
class MethodName(Enum):
    propensity_score_stratification = 'backdoor.propensity_score_stratification' #<--- This is only for binary treatments
    linear_regression = 'backdoor.linear_regression'
    propensity_score_weighting = 'backdoor.propensity_score_weighting' #<--- This is only for binary treatments

class TargetUnit(Enum):
    atc = 'atc' #Causal effect on the control group
    ate = 'ate' #Average Treatment Effect
    att = 'att'

class RefuteEstimate(Enum):
    random_common_cause = 'random_common_cause' #Add Random Common Cause:
    add_unobserved_common_cause = 'add_unobserved_common_cause' #Add Unobserved Common Causes
    placebo_treatment_refuter = 'placebo_treatment_refuter' #Placebo Treatment
    data_subset_refuter = 'data_subset_refuter' #Removing a random subset of the data

# Cell
class PropensityWeighting(Enum):
    ips_weight = {'weighting_scheme':'ips_weight'} #1.Vanilla Inverse Propensity Score weighting (IPS)
    ips_normalized_weight = {'weighting_scheme':'ips_normalized_weight'} #2.Self-normalized IPS weighting (also known as the Hajek estimator)
    ips_stabilized_weight = {'weighting_scheme':'ips_stabilized_weight'} #3.Stabilized IPS weighting

# Cell
#create the abstract class for causal methods
class CausalCodeGen(ABC):
    #1. Identification
    @abstractmethod
    def identification(self):
        'identify a target estimand under the model'
        pass

    #2. Estimation
    @abstractmethod
    def estimation(self):
        'Estimate causal effect based on the identified estimand'
        pass

    #3. Refuting
    @abstractmethod
    def refuting(self):
        'Refute the obtained estimate'
        pass

    #4. Display
    @abstractmethod
    def display(self):
        pass

# Cell
class CausalCodeGenNoGraph(CausalCodeGen):
    def __init__(self,
            df_data,
            treatment = ['treatment'],
            outcome = 'outcome',
            common_causes = ['confounders']
        ):
        #0. Creating the causal model
        self.model= CausalModel(
                data = df_data,
                treatment = treatment,
                outcome = outcome,
                common_causes = common_causes,
                #effect_modifiers=data["effect_modifier_names"]
            )

     #1. Identification
    def identification(self,proceed_when_unidentifiable=True):
        self.identified_estimand = self.model.identify_effect(proceed_when_unidentifiable=proceed_when_unidentifiable)
        #print(self.identified_estimand)
        print('Identification Done')
        pass

    #2. Estimation
    def estimation(self, method_name, target_units = TargetUnit.ate.value):
        self.estimate = self.model.estimate_effect(
            self.identified_estimand,
            method_name = method_name,
            target_units = target_units
        )
        #print(self.estimate)
        #print("Causal Estimate is " + str(self.estimate.value))
        print('Estimation Done')
        pass

    #3. Refuting
    def refuting(self, method):
        default = "Incorrect method"
        return getattr(self, 'refuting_' + str(method), lambda: default)()

    def refuting_1(self, random_seed = 1):
        '''Adding a random common cause variable
         Does the estimation method change its estimate after
         we add an independent random variable as a common
         cause to the dataset? (Hint: It should not)'''
        res_random=self.model.refute_estimate(
            self.identified_estimand,
            self.estimate,
            method_name = RefuteEstimate.random_common_cause.value,
            random_seed = random_seed
        )
        return res_random

    def refuting_2(self, random_seed = 1):
        '''Adding an unobserved common cause variable
        How sensitive is the effect estimate when we add an
        additional common cause (confounder) to the dataset that is correlated with the treatment and the outcome?
        (Hint: It should not be too sensitive)
        '''
        res_unobserved = self.model.refute_estimate(
            self.identified_estimand,
            self.estimate,
            method_name=RefuteEstimate.add_unobserved_common_cause.value,
            confounders_effect_on_treatment="binary_flip",
            confounders_effect_on_outcome="linear",
            effect_strength_on_treatment=0.01,
            effect_strength_on_outcome=0.02,
            random_seed = random_seed
        )
        return res_unobserved

    def refuting_3(self, random_seed = 1):
        '''Replacing treatment with a random (placebo) variable
        What happens to the estimated causal effect when we replace
        the true treatment variable with an independent random variable?
        (Hint: the effect should go to zero)
        '''
        res_placebo = self.model.refute_estimate(
            self.identified_estimand,
            self.estimate,
            method_name=RefuteEstimate.placebo_treatment_refuter.value,
            placebo_type="permute",
            random_seed = random_seed
        )
        return res_placebo

    def refuting_4(self, random_seed = 1):
        '''Removing a random subset of the data
        Does the estimated effect change significantly
        when we replace the given dataset with a randomly selected subset?
        (Hint: It should not)
        '''
        res_subset = self.model.refute_estimate(
            self.identified_estimand,
            self.estimate,
            method_name = RefuteEstimate.data_subset_refuter.value,
            subset_fraction = 0.9,
            random_seed = random_seed
        )
        return res_subset

    #4. Display
    def display(self):
        self.model.view_model()

# Cell
class CausalCodeGenIV(CausalCodeGen):
    def __init__(self,
            df_data,
            treatment = ['treatment'],
            outcome = 'outcome',
            common_causes = ['confounders'],
            instruments = ['instruments']
        ):
        #0. Creating the causal model
        self.model= CausalModel(
                data = df_data,
                treatment = treatment,
                outcome = outcome,
                common_causes = common_causes,
                instruments = instruments
                #effect_modifiers=data["effect_modifier_names"]
            )

     #1. Identification
    def identification(self,proceed_when_unidentifiable=True):
        self.identified_estimand = self.model.identify_effect(proceed_when_unidentifiable=proceed_when_unidentifiable)
        #print(self.identified_estimand)
        print('Identification Done')
        pass

    #2. Estimation
    def estimation(self, method_name='iv.instrumental_variable', target_units = TargetUnit.ate.value):
        self.estimate = self.model.estimate_effect(
            self.identified_estimand,
            method_name = method_name,
            target_units = target_units
        )
        #print(self.estimate)
        #print("Causal Estimate is " + str(self.estimate.value))
        print('Estimation Done')
        pass

    #3. Refuting
    def refuting(self, method):
        default = "Incorrect method"
        return getattr(self, 'refuting_' + str(method), lambda: default)()

    def refuting_1(self, random_seed = 1):
        '''Adding a random common cause variable
         Does the estimation method change its estimate after
         we add an independent random variable as a common
         cause to the dataset? (Hint: It should not)'''
        res_random=self.model.refute_estimate(
            self.identified_estimand,
            self.estimate,
            method_name = RefuteEstimate.random_common_cause.value,
            random_seed = random_seed
        )
        return res_random

    def refuting_2(self, random_seed = 1):
        '''Adding an unobserved common cause variable
        How sensitive is the effect estimate when we add an
        additional common cause (confounder) to the dataset that is correlated with the treatment and the outcome?
        (Hint: It should not be too sensitive)
        '''
        res_unobserved = self.model.refute_estimate(
            self.identified_estimand,
            self.estimate,
            method_name=RefuteEstimate.add_unobserved_common_cause.value,
            confounders_effect_on_treatment="binary_flip",
            confounders_effect_on_outcome="linear",
            effect_strength_on_treatment=0.01,
            effect_strength_on_outcome=0.02,
            random_seed = random_seed
        )
        return res_unobserved

    def refuting_3(self, random_seed = 1):
        '''Replacing treatment with a random (placebo) variable
        What happens to the estimated causal effect when we replace
        the true treatment variable with an independent random variable?
        (Hint: the effect should go to zero)
        '''
        res_placebo = self.model.refute_estimate(
            self.identified_estimand,
            self.estimate,
            method_name=RefuteEstimate.placebo_treatment_refuter.value,
            placebo_type="permute",
            random_seed = random_seed
        )
        return res_placebo

    def refuting_4(self, random_seed = 1):
        '''Removing a random subset of the data
        Does the estimated effect change significantly
        when we replace the given dataset with a randomly selected subset?
        (Hint: It should not)
        '''
        res_subset = self.model.refute_estimate(
            self.identified_estimand,
            self.estimate,
            method_name = RefuteEstimate.data_subset_refuter.value,
            subset_fraction = 0.9,
            random_seed = random_seed
        )
        return res_subset

    #4. Display
    def display(self):
        self.model.view_model()

# Cell
class CausalCodeGenMultiple(CausalCodeGen):
    def __init__(self,
            df_data,
            treatment = ['treatment'],
            outcome = 'outcome',
            common_causes = ['confounders']
        ):
        #0. Creating the causal model
        self.model= CausalModel(
                data = df_data,
                treatment = treatment,
                outcome = outcome,
                common_causes = common_causes,
                #effect_modifiers=data["effect_modifier_names"]
            )

     #1. Identification
    def identification(self,proceed_when_unidentifiable=True):
        self.identified_estimand = self.model.identify_effect(proceed_when_unidentifiable=proceed_when_unidentifiable)
        print(self.identified_estimand)
        print('Identification Done')
        pass

    #2. Estimation
    def estimation(self, target_units = TargetUnit.ate.value):
        self.estimate = self.model.estimate_effect(
            self.identified_estimand,
            method_name =  MethodName.linear_regression.value,
            target_units = target_units,
            method_params={'need_conditional_estimates': False} #No Effect Modifiers Proposed
        )
        print(self.estimate)
        print("Causal Estimate is " + str(self.estimate.value))
        print('Estimation Done')
        pass

    #3. Refuting
    def refuting(self, method):
        default = "Incorrect method"
        return getattr(self, 'refuting_' + str(method), lambda: default)()

    def refuting_1(self, random_seed = 1):
        '''Adding a random common cause variable
         Does the estimation method change its estimate after
         we add an independent random variable as a common
         cause to the dataset? (Hint: It should not)'''
        res_random=self.model.refute_estimate(
            self.identified_estimand,
            self.estimate,
            method_name = RefuteEstimate.random_common_cause.value,
            random_seed = random_seed
        )
        return res_random

    def refuting_2(self, random_seed = 1):
        '''Adding an unobserved common cause variable
        How sensitive is the effect estimate when we add an
        additional common cause (confounder) to the dataset that is correlated with the treatment and the outcome?
        (Hint: It should not be too sensitive)
        '''
        res_unobserved = self.model.refute_estimate(
            self.identified_estimand,
            self.estimate,
            method_name=RefuteEstimate.add_unobserved_common_cause.value,
            confounders_effect_on_treatment="binary_flip",
            confounders_effect_on_outcome="linear",
            effect_strength_on_treatment=0.01,
            effect_strength_on_outcome=0.02,
            random_seed = random_seed
        )
        return res_unobserved

    def refuting_3(self, random_seed = 1):
        '''Replacing treatment with a random (placebo) variable
        What happens to the estimated causal effect when we replace
        the true treatment variable with an independent random variable?
        (Hint: the effect should go to zero)
        '''
        res_placebo = self.model.refute_estimate(
            self.identified_estimand,
            self.estimate,
            method_name=RefuteEstimate.placebo_treatment_refuter.value,
            #placebo_type="permute",
            random_seed = random_seed
        )
        return res_placebo

    def refuting_4(self, random_seed = 1):
        '''Removing a random subset of the data
        Does the estimated effect change significantly
        when we replace the given dataset with a randomly selected subset?
        (Hint: It should not)
        '''
        res_subset = self.model.refute_estimate(
            self.identified_estimand,
            self.estimate,
            method_name = RefuteEstimate.data_subset_refuter.value,
            subset_fraction = 0.9,
            random_seed = random_seed
        )
        return res_subset

    #4. Display
    def display(self):
        self.model.view_model()