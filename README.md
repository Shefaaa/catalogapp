
# Catalog App Project
Create a Book Category app where users can add, edit, and delete books items in the App.

<h3>Technologies Used</h3>
<ul>
  <li><a href="https://www.python.org/" target="_blank">Python 2.7 </a>- Language the project is coded in</li>
  <li><a href="https://www.vagrantup.com/" target="_blank">Vagrant </a>- For a dev VM</li>
  <li><a href="https://www.virtualbox.org/" target="_blank">VirtualBox </a>- Required for Vagrant</li>
  <li><a href="https://git-scm.com/" target="_blank">Git </a>- Source code management</li>
</ul>


<h3>System setup and how to view this project</h3>
<ul>
  <li>Download and install Vagrant</li>
  <li>Download and install Virtual Box</li>
  <li>Clone this repository</li>
  <li>Run <code>vagrant up</code> command to start up the VM</li>
  <li>Run <code>vagrant ssh</code> command to log into the VM.</li>
  <li><code>cd /vagrant </code>to change to your vagrant directory</li>
  <li>Move inside the catalog folder <code>cd /vagrant/catalog</code></li>
  <li>Initialize the database <code>$ Python database_setup.py</code></li>
  <li>Populate the database with some initial data <code>$ Python seeds.py</code></li>
  <li>Run <code>python project.py</code></li>
  <li>Browse the App at this URL <code>http://localhost:8000</code></li>
</ul>

<h3>JSON endpoints:</h3>
<strong>Returns JSON of all categories</strong>
<pre><code>/catalog/categories/json</code></pre>

<strong>Returns JSON of all the items in a specific category</strong>
<pre><code>/catalog/&lt;int:category_id&gt;/items/json</code></pre>

<strong>Returns JSON of item setails in a specific category</strong>
<pre><code>/catalog/&lt;int:item_id&gt;/itemdetails/json</code></pre>


<h3>Helpful Resources</h3>
<ul>
  <li><a href="https://www.python.org/dev/peps/pep-0008/">PEP8 style guide</a></li>
</ul>  
