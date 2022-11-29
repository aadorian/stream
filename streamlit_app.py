import os.path

import math
import pandas as pd
import numpy as np
import streamlit as st
import base64
import textwrap
import lorem #generate lorem ipsum text
import hashlib # hash the tag of the researcher
import altair as alt
import streamlit.components.v1 as components
import time

from io import StringIO
from collections import namedtuple
from git import Repo,  Actor
from PIL import Image, ImageEnhance
from streamlit_extras.dataframe_explorer import dataframe_explorer
from pathlib import Path
from streamlit_timeline import timeline


##1c64f4
#https://i.imgur.com/NrQRoYS.png

IMAGE = Image.open(r"graffiti.png")
IMAGE_URL = 'https://i.imgur.com/H0OKZ9w.png'
IMAGE_URL_API = 'https://i.imgur.com/gJrDSXL.jpg'
DATA_URL = "converted.csv"
DATE_COLUMN = "score"

STATIC_THEORETICAL_DESCRIPTION = '''This demonstration paper introduces ONE: a research curation versioning system. 
ONE proposes an environment for curating data-driven projects adopting qualitative and quantitative methodologies used in e-social sciences.
 '''


st.set_page_config(
    page_title="One",
    page_icon="🧊",

)

STATIC_FOOTER = """ 
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />
<footer class="bg-white rounded-lg shadow sm:flex sm:items-center sm:justify-between p-4 sm:p-6 xl:p-8 dark:bg-gray-800">
  <p class="mb-4 text-sm text-center text-gray-500 dark:text-gray-400 sm:mb-0">
      &copy; 2022 <a href="https://localhost" class="hover:underline" target="_blank">ONE: </a>research curation versioning system.
  </p>
  <div class="flex justify-center items-center space-x-1">
    <a href="#" data-tooltip-target="tooltip-facebook" class="inline-flex justify-center p-2 text-gray-500 rounded-lg cursor-pointer dark:text-gray-400 dark:hover:text-white hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600">
        <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path fill-rule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clip-rule="evenodd" />
        </svg>
        <span class="sr-only">Facebook</span>
    </a>
    <div id="tooltip-facebook" role="tooltip" class="inline-block absolute invisible z-10 py-2 px-3 text-sm font-medium text-white bg-gray-900 rounded-lg shadow-sm opacity-0 transition-opacity duration-300 tooltip dark:bg-gray-700">
        Like us on Facebook
        <div class="tooltip-arrow" data-popper-arrow></div>
    </div>
    <a href="#" data-tooltip-target="tooltip-twitter" class="inline-flex justify-center p-2 text-gray-500 rounded-lg cursor-pointer dark:text-gray-400 dark:hover:text-white hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600">
        <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
        </svg>
        <span class="sr-only">Twitter</span>
    </a>
    <div id="tooltip-twitter" role="tooltip" class="inline-block absolute invisible z-10 py-2 px-3 text-sm font-medium text-white bg-gray-900 rounded-lg shadow-sm opacity-0 transition-opacity duration-300 tooltip dark:bg-gray-700">
        Follow us on Twitter
        <div class="tooltip-arrow" data-popper-arrow></div>
    </div>
    <a href="#" data-tooltip-target="tooltip-github" class="inline-flex justify-center p-2 text-gray-500 rounded-lg cursor-pointer dark:text-gray-400 dark:hover:text-white hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600">
        <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"clip-rule="evenodd" />
        </svg>
        <span class="sr-only">Github</span>
    </a>
    <div id="tooltip-github" role="tooltip" class="inline-block absolute invisible z-10 py-2 px-3 text-sm font-medium text-white bg-gray-900 rounded-lg shadow-sm opacity-0 transition-opacity duration-300 tooltip dark:bg-gray-700">
        Star us on GitHub
        <div class="tooltip-arrow" data-popper-arrow></div>
    </div>
   
</div>
</footer>
"""

STATIC_TIMELINE = """
    <script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />

<div class="p-5 mb-4 bg-gray-50 rounded-lg border border-gray-100 dark:bg-gray-800 dark:border-gray-700">
    <time class="text-lg font-semibold text-gray-900 dark:text-white">January 13th, 2022</time>
    <ol class="mt-3 divide-y divider-gray-200 dark:divide-gray-700">
        <li>
            <a href="#" class="block items-center p-3 sm:flex hover:bg-gray-100 dark:hover:bg-gray-700">
                <img class="mr-3 mb-3 w-12 h-12 rounded-full sm:mb-0" src="https://i.imgur.com/2SMpRLr.jpg" alt=Regi"/>
                <div class="text-gray-600 dark:text-gray-400">
                    <div class="text-base font-normal"><span class="font-medium text-gray-900 dark:text-white">Regi</span> likes <span class="font-medium text-gray-900 dark:text-white">Bonnie Green's</span> post in <span class="font-medium text-gray-900 dark:text-white"> How to start with Flowbite library</span></div>
                    <div class="text-sm font-normal">"I wanted to share a webinar zeroheight."</div>
                    <span class="inline-flex items-center text-xs font-normal text-gray-500 dark:text-gray-400">
                        <svg aria-hidden="true" class="mr-1 w-3 h-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.083 9h1.946c.089-1.546.383-2.97.837-4.118A6.004 6.004 0 004.083 9zM10 2a8 8 0 100 16 8 8 0 000-16zm0 2c-.076 0-.232.032-.465.262-.238.234-.497.623-.737 1.182-.389.907-.673 2.142-.766 3.556h3.936c-.093-1.414-.377-2.649-.766-3.556-.24-.56-.5-.948-.737-1.182C10.232 4.032 10.076 4 10 4zm3.971 5c-.089-1.546-.383-2.97-.837-4.118A6.004 6.004 0 0115.917 9h-1.946zm-2.003 2H8.032c.093 1.414.377 2.649.766 3.556.24.56.5.948.737 1.182.233.23.389.262.465.262.076 0 .232-.032.465-.262.238-.234.498-.623.737-1.182.389-.907.673-2.142.766-3.556zm1.166 4.118c.454-1.147.748-2.572.837-4.118h1.946a6.004 6.004 0 01-2.783 4.118zm-6.268 0C6.412 13.97 6.118 12.546 6.03 11H4.083a6.004 6.004 0 002.783 4.118z" clip-rule="evenodd"></path></svg>
                        Public
                    </span> 
                </div>
            </a>
        </li>
        <li>
            <a href="#" class="block items-center p-3 sm:flex hover:bg-gray-100 dark:hover:bg-gray-700">
                <img class="mr-3 mb-3 w-12 h-12 rounded-full sm:mb-0" src="https://i.imgur.com/2SMpRLr.jpg" alt="Bonnie Green image"/>
                <div>
                    <div class="text-base font-normal text-gray-600 dark:text-gray-400"><span class="font-medium text-gray-900 dark:text-white">Regi</span> react to <span class="font-medium text-gray-900 dark:text-white">Thomas Lean's</span> comment</div>
                    <span class="inline-flex items-center text-xs font-normal text-gray-500 dark:text-gray-400">
                        <svg aria-hidden="true" class="mr-1 w-3 h-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd"></path><path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z"></path></svg>
                        Private
                    </span> 
                </div>
            </a>
        </li>
    </ol>
</div>
<div class="p-5 bg-gray-50 rounded-lg border border-gray-100 dark:bg-gray-800 dark:border-gray-700">
    <time class="text-lg font-semibold text-gray-900 dark:text-white">January 12th, 2022</time>
    <ol class="mt-3 divide-y divider-gray-200 dark:divide-gray-700">
        <li>
            <a href="#" class="block items-center p-3 sm:flex hover:bg-gray-100 dark:hover:bg-gray-700">
                <img class="mr-3 mb-3 w-12 h-12 rounded-full sm:mb-0" src="https://i.imgur.com/X2dXVZM.jpg" alt="Geno"/>
                <div class="text-gray-600 dark:text-gray-400">
                    <div class="text-base font-normal"><span class="font-medium text-gray-900 dark:text-white">Geno</span> likes <span class="font-medium text-gray-900 dark:text-white">Bonnie Green's</span> post in <span class="font-medium text-gray-900 dark:text-white"> How to start with Flowbite library</span></div>
                    <div class="text-sm font-normal">"I wanted to share a webinar zeroheight."</div>
                    <span class="inline-flex items-center text-xs font-normal text-gray-500 dark:text-gray-400">
                        <svg aria-hidden="true" class="mr-1 w-3 h-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd"></path><path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z"></path></svg>
                        Private
                    </span> 
                </div>
            </a>
        </li>
        
       
    </ol>
</div>
"""
STATIC_AVATAR = """
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />

<!-- A few examples from Hero Icons -->
         <div class="mx-auto max-w-screen-sm text-center mb-8 lg:mb-16">
           <h3 class="mb-4 text-2xl tracking-tight font-extrabold text-gray-900 dark:text-white">Our Team</h3>
          <p class="font-light text-gray-500 lg:mb-16 sm:text-xl dark:text-gray-400">MENTOR seMantic Exploration aNd curaTion of  Open hybrid Research</p>
      </div> 
      <div class="grid gap-8 mb-6 lg:mb-16 md:grid-cols-2">
          <div class="items-center bg-gray-50 rounded-lg shadow sm:flex dark:bg-gray-800 dark:border-gray-700">
              <a href="#">
                  <img class="w-80 rounded-lg sm:rounded-none sm:rounded-l-lg" src="https://i.imgur.com/LwlmCLp.jpg" alt="Researcher Avatar">
              </a>
              <div class="p-5">
                  <h5 class="text-xs font-bold tracking-tight text-gray-900 dark:text-white">
                      <a href="#">Genoveva Vargas-Solar</a>
                  </h5>
                  <span class="text-xs text-gray-500 dark:text-gray-400">Research Scientist, CNRS, France</span>                
                  <p class="text-xs font-light text-gray-500 dark:text-gray-400">Senior scientist of the French Council of Scientific Research (CNRS) and a member of the DataBase group of the Laboratory on Informatics on Image and Information Systems (LIRIS).</p>
                  <ul class="flex sm:justify-right space-x-2 sm:mt-0">
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clip-rule="evenodd" /></svg>
                          </a>
                      </li>
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" /></svg>
                          </a>
                      </li>
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" /></svg>
                          </a>
                      </li>
                  </ul>
              </div>
          </div>  
      </div>  
  </div>
</section>
"""

STATIC_POPOVER = """
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />


<p class="flex items-center text-sm font-light text-gray-500 dark:text-gray-400">This is just some informational text <button data-popover-target="popover-description" data-popover-placement="bottom-end" type="button"><svg class="w-4 h-4 ml-2 text-gray-400 hover:text-gray-500" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd"></path></svg><span class="sr-only">Show information</span></button></p>
<div data-popover id="popover-description" role="tooltip" class="absolute z-10 invisible inline-block text-sm font-light text-gray-500 transition-opacity duration-300 bg-white border border-gray-200 rounded-lg shadow-sm opacity-0 w-72 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400">
    <div class="p-3 space-y-2">
        <h3 class="font-semibold text-gray-900 dark:text-white">Activity growth - Incremental</h3>
        <p>Report helps navigate cumulative growth of community activities. Ideally, the chart should have a growing trend, as stagnating chart signifies a significant decrease of community activity.</p>
        <h3 class="font-semibold text-gray-900 dark:text-white">Calculation</h3>
        <p>For each date bucket, the all-time volume of activities is calculated. This means that activities in period n contain all activities up to period n, plus the activities generated by your community in period.</p>
        <a href="#" class="flex items-center font-medium text-blue-600 dark:text-blue-500 dark:hover:text-blue-600 hover:text-blue-700">Read more <svg class="w-4 h-4 ml-1" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path></svg></a>
    </div>
    <div data-popper-arrow></div>
</div>

"""
STATIC_FAQ =    """
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />


<div class="w-full bg-white border rounded-lg shadow-md dark:bg-gray-800 dark:border-gray-700">
    <div class="sm:hidden">
        <label for="tabs" class="sr-only">Select tab</label>
        <select id="tabs" class="bg-gray-50 border-0 border-b border-gray-200 text-gray-900 text-sm rounded-t-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
            <option>Versioning</option>
            <option>Proposal</option>
            <option>Help/option>
        </select>
    </div>
    <ul class="hidden text-sm font-medium text-center text-gray-500 divide-x divide-gray-200 rounded-lg sm:flex dark:divide-gray-600 dark:text-gray-400" id="fullWidthTab" data-tabs-toggle="#fullWidthTabContent" role="tablist">
        <li class="w-full">
            <button id="stats-tab" data-tabs-target="#stats" type="button" role="tab" aria-controls="stats" aria-selected="true" class="inline-block w-full p-4 rounded-tl-lg bg-gray-50 hover:bg-gray-100 focus:outline-none dark:bg-gray-700 dark:hover:bg-gray-600">Stats</button>
        </li>
        <li class="w-full">
            <button id="about-tab" data-tabs-target="#about" type="button" role="tab" aria-controls="about" aria-selected="false" class="inline-block w-full p-4 bg-gray-50 hover:bg-gray-100 focus:outline-none dark:bg-gray-700 dark:hover:bg-gray-600">Objectives</button>
        </li>
        <li class="w-full">
            <button id="faq-tab" data-tabs-target="#faq" type="button" role="tab" aria-controls="faq" aria-selected="false" class="inline-block w-full p-4 rounded-tr-lg bg-gray-50 hover:bg-gray-100 focus:outline-none dark:bg-gray-700 dark:hover:bg-gray-600">Help</button>
        </li>
    </ul>
    <div id="fullWidthTabContent" class="border-t border-gray-200 dark:border-gray-600">
        <div class="hidden p-4 bg-white rounded-lg md:p-8 dark:bg-gray-800" id="stats" role="tabpanel" aria-labelledby="stats-tab">
            <dl class="grid max-w-screen-xl grid-cols-2 gap-8 p-4 mx-auto text-gray-900 sm:grid-cols-3 xl:grid-cols-6 dark:text-white sm:p-8">
                <div class="flex flex-col items-center justify-center">
                    <dt class="mb-2 text-3xl font-extrabold">20</dt>
                    <dd class="font-light text-gray-500 dark:text-gray-400">Researchers</dd>
                </div>
                <div class="flex flex-col items-center justify-center">
                    <dt class="mb-2 text-3xl font-extrabold">117+</dt>
                    <dd class="font-light text-gray-500 dark:text-gray-400">Resources</dd>
                </div>
                <div class="flex flex-col items-center justify-center">
                    <dt class="mb-2 text-3xl font-extrabold">100</dt>
                    <dd class="font-light text-gray-500 dark:text-gray-400">Commits</dd>
                </div>
                <div class="flex flex-col items-center justify-center">
                    <dt class="mb-2 text-3xl font-extrabold">3 </dt>
                    <dd class="font-light text-gray-500 dark:text-gray-400">Releases</dd>
                </div>
                <div class="flex flex-col items-center justify-center">
                    <dt class="mb-2 text-3xl font-extrabold">2+</dt>
                    <dd class="font-light text-gray-500 dark:text-gray-400">Founding</dd>
                </div>
                <div class="flex flex-col items-center justify-center">
                    <dt class="mb-2 text-3xl font-extrabold">4</dt>
                    <dd class="font-light text-gray-500 dark:text-gray-400">Universities</dd>
                </div>
            </dl>
        </div>
        <div class="hidden p-4 bg-white rounded-lg md:p-8 dark:bg-gray-800" id="about" role="tabpanel" aria-labelledby="about-tab">
            <h2 class="mb-5 text-2xl font-extrabold tracking-tight text-gray-900 dark:text-white">ONE: Research Curation Versioning System</h2>
            <!-- List -->
            <ul role="list" class="space-y-4 text-gray-500 dark:text-gray-400">
                <li class="flex space-x-2">
                    <!-- Icon -->
                    <svg class="flex-shrink-0 w-4 h-4 text-blue-600 dark:text-blue-500" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                    <span class="font-light leading-tight">Give insights of the underlining concepts of research process.</span>
                </li>
           
                <li class="flex space-x-2">
                    <!-- Icon -->
                    <svg class="flex-shrink-0 w-4 h-4 text-blue-600 dark:text-blue-500" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                    <span class="font-light leading-tight">Explore in real time of the data that is generated by AI artefacts in the GUI.</span>
                </li>
                <li class="flex space-x-2">
                    <!-- Icon -->
                    <svg class="flex-shrink-0 w-4 h-4 text-blue-600 dark:text-blue-500" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                    <span class="font-light leading-tight">Propose other curation strategies for the underling concepts</span>
                </li>
            </ul>
        </div>
        <div class="hidden p-4 bg-white rounded-lg md:p-8 dark:bg-gray-800" id="faq" role="tabpanel" aria-labelledby="faq-tab">
            <div id="accordion-flush" data-accordion="collapse" data-active-classes="bg-white dark:bg-gray-800 text-gray-900 dark:text-white" data-inactive-classes="text-gray-500 dark:text-gray-400">
                <h2 id="accordion-flush-heading-1">
                    <button type="button" class="flex items-center justify-between w-full py-5 font-medium text-left text-gray-500 border-b border-gray-200 dark:border-gray-700 dark:text-gray-400" data-accordion-target="#accordion-flush-body-1" aria-expanded="true" aria-controls="accordion-flush-body-1">
                    <span>What use case example will be shown?</span>
                    <svg data-accordion-icon class="w-6 h-6 rotate-180 shrink-0" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                    </button>
                </h2>
                <div id="accordion-flush-body-1" class="hidden" aria-labelledby="accordion-flush-heading-1">
                    <div class="py-5 font-light border-b border-gray-200 dark:border-gray-700">
                    <p class="mb-2 text-gray-500 dark:text-gray-400">
                    <b>Use Case</b>:  <strong>As a researcher</strong> <em> I want to </em> keep track of the rationale  of the changes  of research questions, methods, findings and track research feedback from applying ML|AI Algorithms  <em> in order to </em> get a curated version of my research project.
                   </p>
                    <p class="text-gray-500 dark:text-gray-400">Edit <a href="https://hackmd.io/@B-gx5IJ2R2SXlYuuqgRICg/rJn9-H2Uj/edit" class="text-blue-600 dark:text-blue-500 hover:underline">Online Edit</a></p>
                    </div>
                </div>
            
            
                <h2 id="accordion-flush-heading-3">
                    <button type="button" class="flex items-center justify-between w-full py-5 font-medium text-left text-gray-500 border-b border-gray-200 dark:border-gray-700 dark:text-gray-400" data-accordion-target="#accordion-flush-body-3" aria-expanded="false" aria-controls="accordion-flush-body-3">
                    <span>How to design human-in-the-loop (HITL) based workflows that can semi-automate hybrid research methods, including data collections query, exploration and curation?</span>
                    <svg data-accordion-icon class="w-6 h-6 shrink-0" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                    </button>
                </h2>
                <div id="accordion-flush-body-3" class="hidden" aria-labelledby="accordion-flush-heading-3">
                    <div class="py-5 font-light border-b border-gray-200 dark:border-gray-700">
                    <p class="mb-2 text-gray-500 dark:text-gray-400">Lorem ipsum</p>
                    </div>
                </div>
                </div>
        </div>
    </div>
</div>

"""

def hash(a_string):
    hashed_string = hashlib.sha256(a_string.encode('utf-8')).hexdigest()

    return hashed_string

def get_theoretical_framework(description):
    return f"""
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />

<h1 class="mb-4 text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-5xl lg:text-6xl dark:text-white">
ONE <mark class="px-2 text-white bg-blue-600 rounded dark:bg-blue-500">
Research</mark> 
Curation Versioning System</h1>

<p class="mb-3 font-light text-gray-500 dark:text-gray-400">{description}</p>
<!--p class="font-light text-gray-500 dark:text-gray-400">{description}</p-->

"""
STATIC_RESEACH_WORKFLOW = """
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />

<p class="flex items-center text-sm font-light text-gray-500 dark:text-gray-400">
    Problem Statement<button data-popover-target="popover-description" data-popover-placement="bottom-end" type="button"><svg class="w-4 h-4 ml-2 text-gray-400 hover:text-gray-500" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd"></path></svg><span class="sr-only">Show information</span></button></p>
<div data-popover id="popover-description" role="tooltip" class="absolute z-10 invisible inline-block text-sm font-light text-gray-500 transition-opacity duration-300 bg-white border border-gray-200 rounded-lg shadow-sm opacity-0 w-72 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400">
    <div class="p-3 space-y-2">
        <h3 class="font-semibold text-gray-900 dark:text-white">Activity growth - Incremental</h3>
        <p>here is technically a limit, but it's quite large. The padding scheme used for SHA-256 requires that the size of the input (in bits) be expressed as a 64-bit number. Therefore, the maximum size is (264-1)/8 bytes ~= 2'091'752 terabytes.</p>
        <h3 class="font-semibold text-gray-900 dark:text-white">Calculation</h3>
        <p>For each date bucket, the all-time volume of activities is calculated. This means that activities in period n contain all activities up to period n, plus the activities generated by your community in period.</p>
        <a href="#" class="flex items-center font-medium text-blue-600 dark:text-blue-500 dark:hover:text-blue-600 hover:text-blue-700">Read more <svg class="w-4 h-4 ml-1" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path></svg></a>
    </div>
    <div data-popper-arrow></div>
</div>

<p class="flex items-center text-sm font-light text-gray-500 dark:text-gray-400">
    Data Acquisition <button data-popover-target="popover-description2" data-popover-placement="bottom-end" type="button"><svg class="w-4 h-4 ml-2 text-gray-400 hover:text-gray-500" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd"></path></svg><span class="sr-only">Show information</span></button></p>
<div data-popover id="popover-description2" role="tooltip" class="absolute z-10 invisible inline-block text-sm font-light text-gray-500 transition-opacity duration-300 bg-white border border-gray-200 rounded-lg shadow-sm opacity-0 w-72 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400">
    <div class="p-3 space-y-2">
        <h3 class="font-semibold text-gray-900 dark:text-white">Activity growth - Incremental</h3>
        <p>Report helps navigate cumulative growth of community activities. Ideally, the chart should have a growing trend, as stagnating chart signifies a significant decrease of community activity.</p>
        <h3 class="font-semibold text-gray-900 dark:text-white">Calculation</h3>
        <p>For each date bucket, the all-time volume of activities is calculated. This means that activities in period n contain all activities up to period n, plus the activities generated by your community in period.</p>
        <a href="#" class="flex items-center font-medium text-blue-600 dark:text-blue-500 dark:hover:text-blue-600 hover:text-blue-700">Read more <svg class="w-4 h-4 ml-1" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path></svg></a>
    </div>
    <div data-popper-arrow></div>
</div>
"""
STATIC_VERSION_RELEASE = """
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />
<span class="bg-gray-100 text-gray-800 text-xs font-medium inline-flex items-center px-2.5 py-0.5 rounded mr-2 dark:bg-gray-700 dark:text-gray-300">
  <svg aria-hidden="true" class="mr-1 w-3 h-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"></path></svg>
  3 days ago
</span>
<span class="inline-flex items-center p-1 mr-2 text-sm font-semibold text-gray-800 bg-gray-100 rounded-full dark:bg-gray-700 dark:text-gray-300">
  <svg aria-hidden="true" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
  <span class="sr-only">Icon description</span>
</span>
<ol class="relative border-l border-gray-200 dark:border-gray-700">                  
    <li class="mb-10 ml-4">
        <div class="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -left-1.5 border border-white dark:border-gray-900 dark:bg-gray-700"></div>
        <time class="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">July 2022</time>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Research Version v2.0.0</h3>
        <p class="mb-4 text-base font-normal text-gray-500 dark:text-gray-400">Description on version v2.0.0</p>
        <a href="#" class="inline-flex items-center py-2 px-4 text-sm font-medium text-gray-900 bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:outline-none focus:ring-gray-200 focus:text-blue-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700 dark:focus:ring-gray-700">Download Release V2.0.0 <svg class="ml-2 w-3 h-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg></a>
    </li>
    <li class="mb-10 ml-4">
        <div class="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -left-1.5 border border-white dark:border-gray-900 dark:bg-gray-700"></div>
        <time class="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">March 2022</time>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Research Version v1.0.0</h3>
        <p class="text-base font-normal text-gray-500 dark:text-gray-400">Description of Research Version v1.0.0</p>
    </li>
</ol>

"""

STATIC_HR = """
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />

<hr class="my-8 h-px bg-gray-200 border-0 dark:bg-gray-700">

"""

STATIC_LOGO = """

<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />

<div class="flex items-center space-x-4">
    <img class="w-9 h-9 " src="https://i.imgur.com/qnxWCo0.png" alt="">
    <div class="font-medium dark:text-white">
        <div>ONE</div>
        <div class="text-xs text-gray-400 dark:text-gray-400">Research Curation Versioning System</div>
    </div>
</div>
"""

STATIC_BRANCH = """
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />

<div id="toast-interactive" class="p-4 w-full max-w-xs text-gray-500 bg-white rounded-lg shadow dark:bg-gray-800 dark:text-gray-400" role="alert">
    <div class="flex">
        <div class="inline-flex flex-shrink-0 justify-center items-center w-8 h-8 text-blue-500 bg-blue-100 rounded-lg dark:text-blue-300 dark:bg-blue-900">
            <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path></svg>
            <span class="sr-only">Refresh icon</span>
        </div>
        <div class="ml-3 text-sm font-normal">
            <span class="mb-1 text-sm font-semibold text-gray-900 dark:text-white">Update available</span>
            <div class="mb-2 text-sm font-normal">A new software version is available for download.</div> 
            <div class="grid grid-cols-2 gap-2">
                <div>
                    <a href="#" class="inline-flex justify-center w-full px-2 py-1.5 text-xs font-medium text-center text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-800">Update</a>
                </div>
                <div>
                    <a href="#" class="inline-flex justify-center w-full px-2 py-1.5 text-xs font-medium text-center text-gray-900 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-gray-200 dark:bg-gray-600 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-700 dark:focus:ring-gray-700">Not now</a> 
                </div>
            </div>    
        </div>
        <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700" data-dismiss-target="#toast-interactive" aria-label="Close">
            <span class="sr-only">Close</span>
            <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
        </button>
    </div>
</div>

"""
STATIC_BADGE = """

<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />
<span class="bg-gray-100 text-gray-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded dark:bg-gray-700 dark:text-gray-300">Hash</span>
"""
STATIC_POPUP = """
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />

<div class="p-5 mb-4 bg-gray-50 rounded-lg border border-gray-100 dark:bg-gray-800 dark:border-gray-700">
    <time class="text-xs font-semibold text-gray-900 dark:text-white">January 13th, 2022</time>
    <ol class="mt-3 divide-y divider-gray-200 dark:divide-gray-700">
        <li>
            <a href="#" class="block items-center p-3 sm:flex hover:bg-gray-100 dark:hover:bg-gray-700">
                <img class="mr-3 mb-3 w-12 h-12 rounded-full sm:mb-0" src="https://i.imgur.com/2SMpRLr.jpg" alt=Regi"/>
                <div class="text-gray-600 dark:text-gray-400">
                    <div class="text-sm font-normal"><span class="font-medium text-gray-900 dark:text-white">
                    Regi</span> commits <span class="font-medium text-gray-900 dark:text-white">Research's</span> branch in <span class="font-medium text-gray-900 dark:text-white"> 
                    project Mentor</span></div>
                    <div class="text-sm font-normal">"add: semantic metadata."</div>
                    <span class="inline-flex items-center text-xs font-normal text-gray-500 dark:text-gray-400">
                        <svg aria-hidden="true" class="mr-1 w-3 h-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.083 9h1.946c.089-1.546.383-2.97.837-4.118A6.004 6.004 0 004.083 9zM10 2a8 8 0 100 16 8 8 0 000-16zm0 2c-.076 0-.232.032-.465.262-.238.234-.497.623-.737 1.182-.389.907-.673 2.142-.766 3.556h3.936c-.093-1.414-.377-2.649-.766-3.556-.24-.56-.5-.948-.737-1.182C10.232 4.032 10.076 4 10 4zm3.971 5c-.089-1.546-.383-2.97-.837-4.118A6.004 6.004 0 0115.917 9h-1.946zm-2.003 2H8.032c.093 1.414.377 2.649.766 3.556.24.56.5.948.737 1.182.233.23.389.262.465.262.076 0 .232-.032.465-.262.238-.234.498-.623.737-1.182.389-.907.673-2.142.766-3.556zm1.166 4.118c.454-1.147.748-2.572.837-4.118h1.946a6.004 6.004 0 01-2.783 4.118zm-6.268 0C6.412 13.97 6.118 12.546 6.03 11H4.083a6.004 6.004 0 002.783 4.118z" clip-rule="evenodd"></path></svg>
                        Public
                    </span> 
                </div>
            </a>
        </li>
        <li>
            <a href="#" class="block items-center p-3 sm:flex hover:bg-gray-100 dark:hover:bg-gray-700">
                <img class="mr-3 mb-3 w-12 h-12 rounded-full sm:mb-0" src="https://i.imgur.com/2SMpRLr.jpg" alt="Bonnie Green image"/>
                <div>
                    <div class="text-sm font-normal text-gray-600 dark:text-gray-400"><span class="font-medium text-gray-900 dark:text-white">
                    Regi</span> clone <span class="font-medium text-gray-900 dark:text-white">
                    researchquestion branch's</span> 
                    branch</div>
                    <span class="inline-flex items-center text-xs font-normal text-gray-500 dark:text-gray-400">
                        <svg aria-hidden="true" class="mr-1 w-3 h-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd"></path><path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z"></path></svg>
                        Private
                    </span> 
                </div>
            </a>
        </li>
    </ol>
</div>
<div class="p-5 bg-gray-50 rounded-lg border border-gray-100 dark:bg-gray-800 dark:border-gray-700">
    <time class="text-xs font-semibold text-gray-900 dark:text-white">January 12th, 2022</time>
    <ol class="mt-3 divide-y divider-gray-200 dark:divide-gray-700">
        <li>
            <a href="#" class="block items-center p-3 sm:flex hover:bg-gray-100 dark:hover:bg-gray-700">
                <img class="mr-3 mb-3 w-12 h-12 rounded-full sm:mb-0" src="https://i.imgur.com/X2dXVZM.jpg" alt="Geno"/>
                <div class="text-gray-600 dark:text-gray-400">
                    <div class="text-sm font-normal"><span class="font-medium text-gray-900 dark:text-white">
                    Geno</span> merge <span class="font-medium text-gray-900 dark:text-white">
                    research branch</span>
                    tagging <span class="font-medium text-gray-900 dark:text-white">
                     version 1.0.0</span></div>
                    <div class="text-sm font-normal">
                    "tag stable version 1.0.0 "</div>
                    <span class="inline-flex items-center text-xs font-normal text-gray-500 dark:text-gray-400">
                        <svg aria-hidden="true" class="mr-1 w-3 h-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd"></path><path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z"></path></svg>
                        Private
                    </span> 
                </div>
            </a>
        </li>
        
       
    </ol>
</div>
"""

def get_static_photo(title,line,url): 
    return f"""
<center>
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />

<div class="max-w-sm bg-white border border-gray-200 rounded-lg shadow-md dark:bg-gray-800 dark:border-gray-700">
    <a href="#">
        <img class="rounded-t-lg" src="{url}" alt="" />
    </a>
    <div class="p-5">
        <a href="#">
            <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{title}</h5>
        </a>
        <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">{line}</p>
        <a href="#" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            Next Artifact
            <svg aria-hidden="true" class="w-4 h-4 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
        </a>
    </div>
</div>
</center>

"""
def get_static_badge(message,count):
    return f"""
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />
<button type="button" class="inline-flex items-center px-5 py-2.5 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
  {message}
  <span class="inline-flex justify-center items-center ml-2 w-4 h-4 text-xs font-semibold text-blue-800 bg-blue-200 rounded-full">
    {count}
  </span>
</button>
"""
def get_static_commit(author,name,message,time):
    return f"""
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />

<ol class="relative border-l border-gray-200 dark:border-gray-700">                  
    <li class="mb-10 ml-6">            
        <span class="flex absolute -left-3 justify-center items-center w-6 h-6 bg-blue-200 rounded-full ring-8 ring-white dark:ring-gray-900 dark:bg-blue-900">
            <img class="w-6 h-8 " src="https://i.imgur.com/9rG7bts.png" alt="annonym"/>
        </span>
        <div class="justify-between items-center p-4 bg-white rounded-lg border border-gray-200 shadow-sm sm:flex dark:bg-gray-700 dark:border-gray-600">
            <time class="mb-1 text-xs font-normal text-gray-400 sm:order-last sm:mb-0"> {time} </time>
            <div class="text-sm font-normal text-gray-500 dark:text-gray-300"> {author} <a href="#" class="font-semibold text-blue-600 dark:text-blue-500 hover:underline"> {name}  </a> tag <span class="bg-gray-100 text-gray-800 text-xs font-normal mr-2 px-2.5 py-0.5 rounded dark:bg-gray-600 dark:text-gray-300">
            {message}
            </span></div>
        </div>
    </li>
</ol>

"""
def get_static_badge2(message,count,message2,count2):
    return f"""
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />
   <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
</svg>
     <button type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center mr-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
  <path fill-rule="evenodd" d="M9.664 1.319a.75.75 0 01.672 0 41.059 41.059 0 018.198 5.424.75.75 0 01-.254 1.285 31.372 31.372 0 00-7.86 3.83.75.75 0 01-.84 0 31.508 31.508 0 00-2.08-1.287V9.394c0-.244.116-.463.302-.592a35.504 35.504 0 013.305-2.033.75.75 0 00-.714-1.319 37 37 0 00-3.446 2.12A2.216 2.216 0 006 9.393v.38a31.293 31.293 0 00-4.28-1.746.75.75 0 01-.254-1.285 41.059 41.059 0 018.198-5.424zM6 11.459a29.848 29.848 0 00-2.455-1.158 41.029 41.029 0 00-.39 3.114.75.75 0 00.419.74c.528.256 1.046.53 1.554.82-.21.324-.455.63-.739.914a.75.75 0 101.06 1.06c.37-.369.69-.77.96-1.193a26.61 26.61 0 013.095 2.348.75.75 0 00.992 0 26.547 26.547 0 015.93-3.95.75.75 0 00.42-.739 41.053 41.053 0 00-.39-3.114 29.925 29.925 0 00-5.199 2.801 2.25 2.25 0 01-2.514 0c-.41-.275-.826-.541-1.25-.797a6.985 6.985 0 01-1.084 3.45 26.503 26.503 0 00-1.281-.78A5.487 5.487 0 006 12v-.54z" clip-rule="evenodd" />
</svg>
 {message}
    <span class="inline-flex justify-center items-center ml-2 w-4 h-4 text-xs font-semibold text-blue-800 bg-blue-200 rounded-full">
    {count}
    </span>
</button>
<button type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
   <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
  <path d="M14 6H6v8h8V6z" />
  <path fill-rule="evenodd" d="M9.25 3V1.75a.75.75 0 011.5 0V3h1.5V1.75a.75.75 0 011.5 0V3h.5A2.75 2.75 0 0117 5.75v.5h1.25a.75.75 0 010 1.5H17v1.5h1.25a.75.75 0 010 1.5H17v1.5h1.25a.75.75 0 010 1.5H17v.5A2.75 2.75 0 0114.25 17h-.5v1.25a.75.75 0 01-1.5 0V17h-1.5v1.25a.75.75 0 01-1.5 0V17h-1.5v1.25a.75.75 0 01-1.5 0V17h-.5A2.75 2.75 0 013 14.25v-.5H1.75a.75.75 0 010-1.5H3v-1.5H1.75a.75.75 0 010-1.5H3v-1.5H1.75a.75.75 0 010-1.5H3v-.5A2.75 2.75 0 015.75 3h.5V1.75a.75.75 0 011.5 0V3h1.5zM4.5 5.75c0-.69.56-1.25 1.25-1.25h8.5c.69 0 1.25.56 1.25 1.25v8.5c0 .69-.56 1.25-1.25 1.25h-8.5c-.69 0-1.25-.56-1.25-1.25v-8.5z" clip-rule="evenodd" />
</svg>
   {message2}
  <span class="inline-flex justify-center items-center ml-2 w-4 h-4 text-xs font-semibold text-blue-800 bg-blue-200 rounded-full">
  {count2}
    </span>
</button>

"""
STATIC_TABLE = """
    <script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />

<div class="overflow-x-auto relative">
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
                <th scope="col" class="py-3 px-6">
                    Research Branch
                </th>
                <th scope="col" class="py-3 px-6">
                    Researcher
                </th>
                <th scope="col" class="py-3 px-6">
                    Tag
                </th>
                <th scope="col" class="py-3 px-6">
                    Date
                </th>
            </tr>
        </thead>
        <tbody>
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th scope="row" class="py-4 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    problem-statement
                </th>
                <td class="py-4 px-6">
                    Regina
                </td>
                <td class="py-4 px-6">
                    add: problem statement
                </td>
                <td class="py-4 px-6">
                    2021-07-01
                </td>
            </tr>
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th scope="row" class="py-4 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    hypothesis
                </th>
                <td class="py-4 px-6">
                    Genoveva
                </td>
                <td class="py-4 px-6">
                    fix: hypothesis context
                </td>
                <td class="py-4 px-6">
                    2021-07-01
                </td>
            </tr>
            <tr class="bg-white dark:bg-gray-800">
                <th scope="row" class="py-4 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    documentation-branch
                </th>
                <td class="py-4 px-6">
                    Alejandro
                </td>
                <td class="py-4 px-6">
                    doc: documentation-branch
                </td>
                <td class="py-4 px-6">
                     2021-07-01
                </td>
            </tr>
        </tbody>
    </table>
</div>

"""
COMMAND = """
st.write('hello')
    """

STATIC_SPINNER = """
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />

<button disabled type="button" class="py-2.5 px-5 mr-2 text-sm font-medium text-gray-900 bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700 inline-flex items-center">
    <svg role="status" class="inline mr-2 w-4 h-4 text-gray-200 animate-spin dark:text-gray-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="#1C64F2"/>
    </svg>
    Loading...
</button>"""
STATIC_BUTTON = """
<script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />
{COMMAND}
<button type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm p-2.5 text-center inline-flex items-center mr-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
  <svg aria-hidden="true" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
  <span class="sr-only">Icon description</span>
</button>
"""
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
def get_static_artifact(tag,paragraph):
    return f'''
    <script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />

<p class="mb-3 font-light text-gray-500 dark:text-gray-400"> {paragraph}</p>
<div class="grid grid-cols-1 md:gap-6 md:grid-cols-2">
    <hr class="my-8 h-px bg-gray-200 border-0 dark:bg-gray-700">
    <blockquote class="mb-3">
    <p class="text-xl italic font-semibold text-gray-900 dark:text-white">
        {tag}
        </p>
    </blockquote>
    <hr class="my-8 h-px bg-gray-200 border-0 dark:bg-gray-700">
</div>
<p class="mb-3 font-light text-gray-500 dark:text-gray-400"></p>
'''

def create_list(map_object):
    string = ''
    for item in map_object:
        string +=    '<li class="flex items-center"> <span class="inline-flex items-center p-1 mr-2 text-sm font-semibold text-gray-800 bg-gray-100 rounded-full dark:bg-gray-700 dark:text-gray-300"> '
        string += item
        string +=   '</li>'
    return string


def get_dinamic_list(list,title): 
    return f""" <script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />
    <h2 class="mb-2 text-lg font-semibold text-gray-900 dark:text-white">{title}</h2>
    <ul class="space-y-1 max-w-md list-inside text-gray-500 dark:text-gray-400">
    {create_list(list)} </ul>""";


def get_static_popover(name,message,title):
    return f'''
        <script src="https://unpkg.com/flowbite@latest/dist/flowbite.js"></script>
<link rel="stylesheet" href="https://unpkg.com/flowbite@latest/dist/flowbite.min.css" />

<button data-popover-target="popover-default" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">{name}</button>
<div data-popover id="popover-default" role="tooltip" class="absolute z-10 invisible inline-block w-64 text-sm font-light text-gray-500 transition-opacity duration-300 bg-white border border-gray-200 rounded-lg shadow-sm opacity-0 dark:text-gray-400 dark:border-gray-600 dark:bg-gray-800">
    <div class="px-3 py-2 bg-gray-100 border-b border-gray-200 rounded-t-lg dark:border-gray-600 dark:bg-gray-700">
        <h3 class="font-semibold text-gray-900 dark:text-white">{title}</h3>
    </div>
    <div class="px-3 py-2">
        <p>{message}</p>
    </div>
    <div data-popper-arrow></div>
</div>
'''



def get_static_heroicon_search():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
</svg>
'''

def get_static_hash():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
  <path fill-rule="evenodd" d="M9.493 2.853a.75.75 0 00-1.486-.205L7.545 6H4.198a.75.75 0 000 1.5h3.14l-.69 5H3.302a.75.75 0 000 1.5h3.14l-.435 3.148a.75.75 0 001.486.205L7.955 14h2.986l-.434 3.148a.75.75 0 001.486.205L12.456 14h3.346a.75.75 0 000-1.5h-3.14l.69-5h3.346a.75.75 0 000-1.5h-3.14l.435-3.147a.75.75 0 00-1.486-.205L12.045 6H9.059l.434-3.147zM8.852 7.5l-.69 5h2.986l.69-5H8.852z" clip-rule="evenodd" />
</svg>
'''
def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s" width="20" height="20"/>' % b64
    st.write(html, unsafe_allow_html=True)

def read_markdown_file(markdown_file):
   return Path(markdown_file).read_text()





#data_load_state = st.text("Loading data...")
data = load_data(10000)
#data_load_state.text("Done!")

repo = Repo.init(".")
git = repo.git
components.html(STATIC_LOGO, height=38)


#
#tab_theoretical_framework, tab_tag, tab_exploration, tab_release, tab_scientist = st.tabs(["Theorethical Framework",  "Tag","Exploration", "Releases","Scientists"])
tab_intro, tab_tag_researcher, tab_tag_ai,tab_exploration, tab_release, tab_scientist, tab_branches = st.tabs(["Intro",  "Researcher Tag","AI Tag", "Exploration", "Releases","Scientists","Branches"])

with tab_branches:
    tab_branches.subheader("Research Branches")
    expander = st.expander("Create Branch")
    with expander:
        branch_name = st.text_input('Name of the branch', 'researcher')
        try:
            git_command = ["git","branch",branch_name]
            result = repo.git.execute(git_command)
            st.caption(branch_name + 'created.')
            git.checkout(branch_name)
        except: 
            print('branch already exists')
        git_command = ["git","branch"]
        result = repo.git.execute(git_command)
        components.html(get_dinamic_list(result.split(),'branches'),height=250)
    #expander = st.expander("Delete Branch")
    #with expander:
         #try:

         #  branch_delete_name = st.text_input('Branch delete', 'delete')
         #  git_command = ["git","branch","-D",branch_delete_name]
        #   result = repo.git.execute(git_command)
        #   components.html(STATIC_SPINNER, height=50)
        #   time.sleep(3)

        # except:
        #    print('cannot delete this branch')
    git.checkout('master')
with tab_exploration:
    render_svg(get_static_heroicon_search())
    tab_exploration.subheader("Exploration")
    st.caption("Exploration")
    components.html(get_static_badge2('branches',2,'AI algorithms',1),height=40)
    expander = st.expander("AI - Google API Cloud Results")    
    with expander:
        st.subheader("Explore AI data")
        df = pd.DataFrame(data, columns=["description", "topicality", "score"])
        filtered_df = dataframe_explorer(data)
        st.dataframe(filtered_df)
        uploaded_file = st.file_uploader("", type=["csv"])
        if uploaded_file is not None:
            st.write(uploaded_file.name)
    expander = st.expander("Versioning Log")    
    with expander:
        st.write(git.status())
        st.write(git.log())
    expander = st.expander("Georeferenced Tags")
    with expander:
        df = pd.DataFrame(
            np.random.randn(1000, 2) / [50, 50] + [-34.909944, -56.2100996],
            columns=['lat', 'lon'])
        st.map(df)
    expander = st.expander("Research Codebook")
    with expander:
        intro_markdown = read_markdown_file("./README.md")
        st.markdown(intro_markdown, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Files",type=['md'])
        if uploaded_file is not None:
            file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
            st.write(file_details)
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            string_data = stringio.read()
            st.write(string_data)
with tab_intro:
   
    git.checkout("master")
    paragraph = lorem.paragraph()
    #st.write(paragraph)
    #lorem_paragraph = lorem.paragraph()s
    components.html(get_theoretical_framework(STATIC_THEORETICAL_DESCRIPTION), height=180)
    st.image('https://i.imgur.com/YLI8rJ8.png', width=200)
with tab_tag_researcher: 
    tab_tag_researcher.subheader("Researcher tags")
    git.checkout("researcher")
    researcher_tag = st.text_input('RITL researcher-in-the-loop', 'Insert here your tag | description')
    if st.button('Commit'):
        st.caption('Commited '+ researcher_tag)
        data = hash('hash 256' + researcher_tag)
        git_command_add = ["git","add",'-A']
        result = repo.git.execute(git_command_add)
        components.html(get_static_commit('author','annonymous', researcher_tag ,data),height=100)
        components.html(STATIC_HR, height=40)
      
        st.caption("Versioning Log")
        index = repo.index
        author = Actor("An author", "author@example.com")
        committer = Actor("A researcher", "committer@researcher.com")
        index.commit(researcher_tag, author=author, committer=committer)
        commits = repo.iter_commits('researcher', max_count=2)
        components.html(STATIC_HR, height=40)
        expander = st.expander("Researcher Tag Logs")
        with expander:
            components.html(get_static_commit('author','annonymous',git.log(),'data'),height=440)
    components.html(STATIC_HR, height=40)
    st.caption("Object of Study")
    components.html(get_static_badge('objects',4),height=40)
    components.html(get_static_photo('Object of Study',lorem.sentence(), IMAGE_URL_API), height=444)
    components.html(get_static_popover('status', git.status(),'researcher'),height=250)
    git.checkout("master")
with tab_tag_ai:
    tab_tag_ai.subheader("AI tags") 
    ai_tag = st.text_input('AI researcher-in-the-loop #', 'Modify AI Feedback')
    components.html(get_static_badge('objects',4),height=40)
    components.html(STATIC_HR, height=40)
    st.caption("Object of Study")
    paragraph = lorem.paragraph()
    components.html(get_static_photo('Object of Study',lorem.sentence(), IMAGE_URL_API), height=444)
    components.html(get_static_popover('AI branch ',lorem.sentence(),'AI'),height=250)
 
    components.html(STATIC_HR, height=40)
    git.checkout("master")
with tab_release:
    tab_release.subheader("Releases")
    st.caption("Releases")
    components.html(get_static_badge('releases',4),height=40)
    output_filename ='repo.zip'
    headcommit = repo.head.commit
    path = '.git'
   # make_tarfile(output_filename, path)
    with open('repo.zip', 'rb') as f:
        st.download_button('Download current version', f, file_name='repo.zip')  # Defaults to 'application/octet-stream'
    components.html(STATIC_VERSION_RELEASE, height=250)
with tab_scientist:
    tab_scientist.subheader("Scientists")
    st.caption("Scientists")
    #components.html(get_static_badge('branches',2),height=40)
    components.html(get_static_badge('researchers',3),height=44)
    components.html(STATIC_AVATAR, height=300)
    if st.button('Reset'):
         git_command_1 = ["git","checkout",'--orphan','latest_branch']
         result = repo.git.execute(git_command_1)
         git_command_2 = ["git","add",'-A']
         result = repo.git.execute(git_command_2)
         git_command_3 = ["git","commit","-am","'commit message'"]
         result = repo.git.execute(git_command_3)
         git_command_4 = ["git","branch","-D","master"]
         result = repo.git.execute(git_command_4)
         git_command_5 = ["git","branch","-m","master"]
         result = repo.git.execute(git_command_5)
         

    
    #index = repo.index
    #author = Actor("An author", "author@example.com")
    #committer = Actor("A committer", "committer@example.com")
    #repo.index.commit("Commited")
# commit by commit message and author and committer
   #index.commit("my commit message", author=author, committer=committer)
#with tab_about: 
#    with st.echo(code_location="below"):
#         st.caption("About ")
#         st.caption("About")
#    components.html(STATIC_FAQ, height=400)

#with tab_timeline:
#    st.caption("Research timeline versions")
    # use full page width
#    with open('example.json', "r") as f:
#        data = f.read()
 
    #timeline(data, height=350)

    #expander = st.expander("About")
    #with expander:
     #   components.html(STATIC_RESEACH_WORKFLOW, height=450)
#with tab_log:
#
#    st.caption("Log")
   
#    with st.echo(code_location="below"):
       # st.caption("About ")
#      components.html(STATIC_POPUP, height=400)
#      components.html(STATIC_TABLE, height=400)

components.html(STATIC_FOOTER, height=200)

