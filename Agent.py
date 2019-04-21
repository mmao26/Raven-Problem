# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image, ImageChops
import math

from RavensObject import RavensObject
import copy
import random

# -------------------------------------  Visual Section Start ----------------------------#

# Utility Functions
def load_images(problem):
    global image_A, image_B, image_C, image_D, image_E, image_F, image_G, image_H
    prob_figs = problem.figures
    for key, value in sorted(prob_figs.iteritems()):
        figure = prob_figs[key]
        file_name = figure.visualFilename
        if key == 'A':
            image_A = Image.open(file_name)
        elif key == 'B':
            image_B = Image.open(file_name)
        elif key == 'C':
            image_C = Image.open(file_name)
        elif key == 'D':
            image_D = Image.open(file_name)
        elif key == 'E':
            image_E = Image.open(file_name)
        elif key == 'F':
            image_F = Image.open(file_name)
        elif key == 'G':
            image_G = Image.open(file_name)
        elif key == 'H':
            image_H = Image.open(file_name)

def get_diffPercentage(img1, img2):
    '''
    Credit to
    http://rosettacode.org/wiki/Percentage_difference_between_images#Python
    '''
    pairs = zip(img1.getdata(), img2.getdata())
    if len(img1.getbands()) == 1:
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))
    ncomponents = img1.size[0] * img1.size[1] * 3
    return (dif / 255.0 * 100) / ncomponents


def get_union(img1, img2):
    return ImageChops.darker(img1, img2)

def get_intersection(img1, img2):
    return ImageChops.lighter(img1, img2)


def get_differences(img1, img2):
    return ImageChops.invert(ImageChops.difference(img1, img2))

# Solver Functions
def solution_union(problem): # [v1] used by problem set E-01, E-02, E-03, E-09
    candidate = -1
    try:
        diff_ABC = get_diffPercentage(get_union(image_A, image_B), image_C)
        diff_DEF = get_diffPercentage(get_union(image_D, image_E), image_F)
        pct_list = []
        if diff_ABC < 5 and diff_DEF < 5: 
            for i in range(1, 9):
                candidate_img = Image.open(problem.figures[str(i)].visualFilename)
                diff_GHx = get_diffPercentage(get_union(image_G, image_H), candidate_img)
                pct_list.append(diff_GHx)
            candidate = pct_list.index(min(pct_list)) + 1
            return candidate
        return candidate
    except:
        return candidate

def solution_intersection(problem): # [v1] used by problem set E-10, E-11 
    candidate = -1
    try:
        diff_ABC = get_diffPercentage(get_intersection(image_A, image_B), image_C)
        diff_DEF = get_diffPercentage(get_intersection(image_D, image_E), image_F)
        pct_list = []
        if diff_ABC < 5 and diff_DEF < 5: 
            for i in range(1, 9):
                candidate_img = Image.open(problem.figures[str(i)].visualFilename)
                diff_GHx = get_diffPercentage(get_intersection(image_G, image_H), candidate_img)
                pct_list.append(diff_GHx)
            candidate = pct_list.index(min(pct_list)) + 1
            return candidate
        return candidate
    except:
        return candidate

def solution_AtoC(problem): # [v1] used by problem set D-01, D-04, D-05, D-06
    candidate = -1
    try:
        diff_AC = get_differences(image_A, image_C)
        pct_list = []
        for i in range(1, 9):
            candidate_img = Image.open(problem.figures[str(i)].visualFilename)
            diff_Gx = get_diffPercentage(diff_AC, get_differences(image_G, candidate_img))
            pct_list.append(diff_Gx)
        candidate = pct_list.index(min(pct_list)) + 1
        return candidate
    except:
        return candidate


def solution_BDandAE(problem): # [v1] used by problem set (D-02), D-07, D-10, (D-11)
    # solution is BD + AE
    candidate = -1
    try:
        # get answer image
        pattern1 = get_intersection(image_B, image_D)
        pattern2 = get_intersection(image_A, image_E)
        ans_img = get_union(pattern1, pattern2)

        # impose some constraints -- skip questions instead of giving wrong answers
        pat1 = get_intersection(image_F, image_H)
        pat2 = get_differences(image_A, pat1)
        pat3 = get_differences(pat2, image_E)
        diff_A = get_diffPercentage(get_union(pat1, pat2), image_A)
        diff_E = get_diffPercentage(get_union(pat3, pat2), image_E)
      
        pct_list = []
        if diff_A < 2 and diff_E < 2:
            for i in range(1, 9):
                candidate_img = Image.open(problem.figures[str(i)].visualFilename)
                diff_pct = get_diffPercentage(ans_img, candidate_img)
                pct_list.append(diff_pct)
            candidate = pct_list.index(min(pct_list)) + 1
            return candidate
        return candidate
    except:
        return candidate

def solution_GtoH(problem): # [v2] used by problem set E-05, E-06, E-07, E-08
    # use of the GH to solve the problem 
    candidate = -1
    try:
        diff_ABC = get_diffPercentage(get_differences(image_A, image_B), image_C)
        diff_GH = get_differences(image_G, image_H)
        pct_list = []
        if diff_ABC < 2:
            for i in range(1, 9):
                candidate_img = Image.open(problem.figures[str(i)].visualFilename)
                diff_pct = get_diffPercentage(diff_GH, candidate_img)
                pct_list.append(diff_pct)
            candidate = pct_list.index(min(pct_list)) + 1
            return candidate
        return candidate
    except:
        return candidate

def solver_problem_D(problem):
    # try to solve problem by using relationship one by one
    
    candidate = solution_BDandAE(problem)
    if candidate > 0:
        return candidate
    
    candidate = solution_AtoC(problem)
    return candidate if candidate > 0 else -1

def solver_problem_E(problem):
    # try to solve problem by using relationship one by one
    
    candidate = solution_union(problem)
    if candidate > 0:
        return candidate
    
    candidate = solution_intersection(problem)
    if candidate > 0:
        return candidate
    
    candidate = solution_GtoH(problem)
    return candidate if candidate > 0 else -1

# -------------------------------------  Visual Section Ends ----------------------------#

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
        self.SIZES = {"very small": 0, "small": 1, "medium": 2, "large": 3, "very large": 4, "huge": 5}
        self.direct1 = False
        self.direct2 = False
        self.exchange = False
        self.new_fig = False
    # ------------------------------------  Verbal Section Starts --------------------------#
    def get_delta_fromAttr(self, attr1, attr2):
        delta = {}
        if "shape" in attr1 and "shape" in attr2:
            if attr1["shape"] != attr2["shape"]:
                delta["shape"] = attr1["shape"] + " to " + attr2["shape"]
        if "fill" in attr1 and "fill" in attr2:
            if attr1["fill"] != attr2["fill"]:
                delta["fill"] = True 
        if "size" in attr1 and "size" in attr2:
            if attr1["size"] != attr2["size"]:
                delta["size"] = self.SIZES[attr1["size"]] - self.SIZES[attr2["size"]]
        if "angle" in attr1 and "angle" in attr2:
            if attr1["angle"] != attr2["angle"]:
                delta["angle"] = abs(int(attr1["angle"]) - int(attr2["angle"]))
        if "alignment" in attr1 and "alignment" in attr2:
            eachLoc_list1 = attr1["alignment"].split("-")
            eachLoc_list2 = attr2["alignment"].split("-")
            #print eachLoc_list1
            #print eachLoc_list2
            diff_count = 0
            for i in range(len(eachLoc_list1)):
                if eachLoc_list1[i] == eachLoc_list2[i]:
                    diff_count += 1
            delta["alignment"] = diff_count
        if "width" in attr1 and "width" in attr2:           
            if attr1["width"] != attr2["width"]:
                delta["width"] = self.SIZES[attr1["width"]] - self.SIZES[attr2["width"]]
                
        if "height" in attr1 and "height" in attr2:
            if attr1["height"] != attr2["height"]:
                delta["height"] = self.SIZES[attr1["height"]] - self.SIZES[attr2["height"]]
                
        if "width" in attr1 and "size" in attr2:
            if self.SIZES[attr1["width"]] - self.SIZES[attr2["size"]] != 0:
                delta["width"] = self.SIZES[attr1["width"]] - self.SIZES[attr2["size"]]
                try:
                    del delta["shape"]
                except:
                    pass
        if "height" in attr1 and "size" in attr2:
            if self.SIZES[attr1["height"]] - self.SIZES[attr2["size"]] != 0:
                delta["height"] = self.SIZES[attr1["height"]] - self.SIZES[attr2["size"]]
                try:
                    del delta["shape"]
                except:
                    pass
        if "above" in attr1 and "above" in attr2:
            delta["above"] = True
        if (len(attr1) == len(attr2)) and ("left-of" in attr1 and "left-of" not in attr2):
            self.direct1 = True
        if (len(attr1) == len(attr2)) and ("left-of" not in attr1 and "left-of" in attr2):
            self.direct2 = True
        if (len(attr1) == len(attr2)) and ("left-of" in attr1 and "overlaps" in attr2):
            self.exchange = True
        return delta

    def get_delta_fromFig(self, fig1, fig2, PSet):
        fig1_objects = copy.copy(fig1.objects)
        fig2_objects = copy.copy(fig2.objects)
        
        delta_set = {}
        if PSet == 'B':
            # for each objects
            for obj1 in fig1_objects:
                delta_set[obj1] = {}
                for obj2 in fig2_objects:
                    delta_set[obj1][obj2] = self.get_delta_fromAttr(fig1_objects[obj1].attributes, fig2_objects[obj2].attributes)
            return delta_set
        elif PSet == 'C':
            # for each objects in order
            
            delta_quantity = len(fig1_objects)-len(fig2_objects)
            
            length = min(len(fig1_objects), len(fig2_objects))
            #print (fig1_objects)
            #print (fig2_objects)
            for i in range(length):
                obj1 = sorted(fig1_objects.iterkeys())[i]
                #obj2 = sorted(fig2_objects.iterkeys())[i]
                obj2 = fig2_objects.keys()[i] if self.exchange and self.new_fig else sorted(fig2_objects.iterkeys())[i]
                
                delta_set[obj1] = {}
                delta_set[obj1][obj2] = self.get_delta_fromAttr(fig1_objects[obj1].attributes, fig2_objects[obj2].attributes)
            self.new_fig = self.exchange
            
            if delta_quantity != 0:           
                for x in range(0, abs(delta_quantity)):
                    name1 = "_EMPTY" + str(x) + "_1"
                    name2 = "_EMPTY" + str(x) + "_2"
                    if delta_quantity > 0:
                        delta_set.update({name1: {name2: {}}})
                    else:
                        delta_set.update({name1: {name2: {}}})
            return delta_set, delta_quantity

    def check_similarity(self, dict1, dict2, method):
        similarity = True
        objNAME_p1f1 = sorted(dict1.iterkeys()) # ['p', 'q', 'r', 's']
        if method == 1:
            objNAME_p2f1 = sorted(dict2.iterkeys()) # ['t', 'u', 'v', 'w']
        else:
            objNAME_p2f1 = dict2.keys()
            
        if len(objNAME_p1f1) != len(objNAME_p2f1):           
            for x in range(0, abs(len(objNAME_p1f1) - len(objNAME_p2f1))):
                name1 = "_EMPTY" + str(x) + "_1"
                name2 = "_EMPTY" + str(x) + "_2"
                if len(objNAME_p1f1) > len(objNAME_p2f1):
                    dict2.update({name1: {name2: {}}})
                else:
                    dict1.update({name1: {name2: {}}})

        else:
            for idx1 in range(len(objNAME_p1f1)):
                objNAME_p1f2 = dict1[objNAME_p1f1[idx1]].keys() # list
                objNAME_p2f2 = dict2[objNAME_p2f1[idx1]].keys() # list

                if len(objNAME_p1f2) != len(objNAME_p2f2):
                    similarity = False
                    return similarity
                else:
                    for idx2 in range(len(objNAME_p1f2)):
                        if dict1[objNAME_p1f1[idx1]][objNAME_p1f2[idx2]] not in dict2[objNAME_p2f1[idx1]].values():
                            similarity = False
                            return similarity
        return similarity
    # -------------------------------------  Verbal Section End ----------------------------#
    def Solve(self,problem):
        print ("--------------------------- "+problem.name+" ----------------------------")
        
        # Project 1 -- Problem Set B (Verbal)
        if problem.problemType == "2x2" and 'Problem B' in problem.name:
            delta_set_AB = self.get_delta_fromFig(problem.figures["A"], problem.figures["B"], 'B')
            for candidate in range(1, 7):
                candidate_delta = self.get_delta_fromFig(problem.figures["C"], problem.figures[str(candidate)], 'B')
                if self.check_similarity(delta_set_AB, candidate_delta, 1):
                    print ("AB -- Solution " + str(candidate))
                    return candidate
            
            # if AB not solve, try AC.
            delta_set_AC = self.get_delta_fromFig(problem.figures["A"], problem.figures["C"], 'B')
            for candidate in range(1, 7):
                candidate_delta = self.get_delta_fromFig(problem.figures["B"], problem.figures[str(candidate)], 'B')
                if self.check_similarity(delta_set_AC, candidate_delta, 1):
                    print ("AC -- Solution " + str(candidate))
                    return candidate
            return -1
        # Project 2 -- Problem Set C (Verbal)
        elif problem.problemType == "3x3" and 'Problem C' in problem.name:

            self.direct1 = False
            self.direct2 = False
            self.exchange = False
            self.new_fig = False

            naive_pool = []
            delta_set_GH, delta_quantity = self.get_delta_fromFig(problem.figures["G"], problem.figures["H"], 'C')
            
            #print (delta_set_GH)
            #print ("G - H: " + str(delta_quantity))
            
            for candidate in range(1, 9):
                candidate_delta, candidate_delta_quantity = self.get_delta_fromFig(problem.figures["H"], problem.figures[str(candidate)], 'C')
                #print ("Candidate_" + str(candidate) + ": delta is " + str(candidate_delta))
                #print ("Candidate_" + str(candidate) + ": delta quantity is " + str(candidate_delta_quantity))

                if delta_quantity == candidate_delta_quantity:
                    naive_pool.append(candidate)
                if self.check_similarity(delta_set_GH, candidate_delta, 1) and delta_quantity == candidate_delta_quantity and (self.direct1 == self.direct2):
                    print ("GH -- Solution " + str(candidate))
                    return candidate
                
            # if not solve, try this
            for candidate in range(1, 9):
                candidate_delta, candidate_delta_quantity = self.get_delta_fromFig(problem.figures["H"], problem.figures[str(candidate)], 'C')
                if delta_quantity == candidate_delta_quantity:
                    naive_pool.append(candidate)
                if self.check_similarity(delta_set_GH, candidate_delta, 2) and delta_quantity == candidate_delta_quantity and (self.direct1 == self.direct2):
                    print ("GH -- Solution " + str(candidate))
                    return candidate
                
            if len(naive_pool) > 0: 
                index = random.randint(0, len(naive_pool)-1)
                candidate = naive_pool[index]
            else:
                candidate = random.randint(1, 8)
            print ("Random Guess " + str(candidate))
            return candidate
        
        # Project 3 -- Problem Set D and E (Visual)
        elif problem.problemType == "3x3" and 'Problem D' in problem.name:
            load_images(problem)
            candidate = solver_problem_D(problem)
            print ("Solution is " + str(candidate))
            return candidate
        
        elif problem.problemType == "3x3" and 'Problem E' in problem.name:
            load_images(problem)
            candidate = solver_problem_E(problem)
            print ("Solution is " + str(candidate))
            return candidate
        
