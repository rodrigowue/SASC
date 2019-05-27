import re
import sys
import networkx as nx
import matplotlib.pyplot as plt

def print_gmelogo():
	print("============================================================");
	print("           .:-.        `..--.``      .         .    ........");
	print(" .        .--/+++`   -++/---:++/.    //       -+`   /+//////");
	print(" `:.      `-/++:.  `/+:       .:`   .++:     -++-   /+.     ");
	print("   /-     +++-     :+:              /+/+-   -+/++   /+:-----");
	print(" `/:      /++/     /+-     .+++++/ `+/ :+- `++`:+.  /+-.....");
	print("-++:.`    `+++-    .++`        :+: -+-  /+-+/` .+/  /+.     ");
	print("++:-.     `/+++`    .++-.` ``-/+:  /+`  `/++`   ++` /+.`````");
	print("/++:` `.:/++++:      `-:/+/+//-`  `/:    `/.    -/. :///////");
	print(" -/++/+++++/-`       ");
	print("   ./++:.`           ");
	print("============================================================");

def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

class Transistor:
	def __init__(self, name,source,gate,drain,bulk,ttype,wsize,fingers,lsize):
		self.name 	= name;
		self.source = source;
		self.gate 	= gate;
		self.drain 	= drain;
		self.bulk 	= bulk;
		self.ttype 	= ttype;
		self.wsize 	= wsize;
		self.fingers = fingers;
		self.lsize 	= lsize;
		self.stack 	= 1;
	#===============================================
	#Methods for Attribute Manipulation
	#===============================================
	def get_name(self):
		return self.name;
	def set_name(self, name):
		self.name = name;
	def get_source(self):
		return self.source;
	def set_source(self,source):
		self.source = source;
	def get_gate(self):
		return self.gate;
	def set_gate(self,gate):
		self.gate = gate;
	def get_drain(self):
		return self.drain;
	def set_drain(self,drain):
		self.drain = drain;
	def get_bulk(self):
		return self.bulk;
	def set_bulk(self,bulk):
		self.bulk = bulk;
	def get_ttype(self):
		return self.ttype;
	def set_ttype(self,ttype):
		self.ttype = ttype;
	def get_wsize(self):
		return self.wsize;
	def set_wsize(self,wsize):
		self.wsize = wsize;
	def get_fingers(self):
		return self.fingers;
	def set_fingers(self,fingers):
		self.fingers = fingers;
	def get_lsize(self):
		return self.lsize;
	def set_lsize(self,lsize):
		self.lsize = lsize;
	def get_stack(self):
		return self.stack;
	def set_stack(self, stack):
		self.stack = stack;


def main():
	print("============================================================");
	print("SPICE PARSER AND AUTOMATIC STACK CALCULATOR");
	print("============================================================");
	print("By: Rodrigo N. Wuerdig");
	print("Contact: rnwuerdig@inf.ufrgs.br");
	print_gmelogo();
	
	
	#===========================================================================
	#Fetch Args
	#===========================================================================
	if (sys.argv[1]==None):
		print("WARNING: ARG1 SHOULD CONTAIN WP/WN RATIO");
		wpwn_ratio=2.0;
	else:
		wpwn_ratio=float(sys.argv[1]);
	if (sys.argv[2]==None):
		print("ERROR: ARG2 SHOULD CONTAIN SPICE FILE");
		return -1;
	else:
		file = sys.argv[2];
	#===========================================================================
	#Open Spice File
	#===========================================================================
	f=open(file,"r");
	ntransistors=[]; #Start List for N Transistors
	ptransistors=[]; #Start List for P Transistors
	inputs=[]; #Start List for Inputs
	outputs=[];  #Start List for Output Nodes
	for line in f:
		newline = line.rstrip('\n');
		#Check if the line starts with *.pininfo
		if "*.pininfo" in newline.lower():
			#Fetches Outputs from the pininfo line
			outpins = re.findall('[a-zA-Z0-9]*:[Oo]', newline);
			#Fetches Inputs from the pininfo line
			inpins = re.findall('[a-zA-Z0-9]*:[Ii]', newline);
			#Fetches Vdd pin from the pininfo line
			vddpin = str(re.search('[a-zA-Z0-9]*:[Pp]', newline)[0]);
			#Fetches Gnd pin from the pininfo line
			gndpin = str(re.search('[a-zA-Z0-9]*:[Gg]', newline)[0]);
			#Check if its missing output pins
			if is_empty(outpins):
				print("pattern not found outputs");
			else:
				for out in outpins:
					print("Output Pins:",out);
					outputs.append(out.replace(':O',''));
			#Check if its missing output pins
			if is_empty(inpins):
				print("pattern not found outputs");
			else:
				for in_pin in inpins:
					print("input Pins:",in_pin);
					inputs.append(in_pin.replace(':O',''));
			#Check if its missing vdd pins
			if is_empty(vddpin):
				print("pattern not found outputs");
				return -3;
			else:
				print("Circuit Supply Pin:", vddpin);
				vddpin=vddpin.replace(':P','');
			#Check if its missing gnd pins
			if is_empty(gndpin):
				print("pattern not found outputs");
				return -3;
			else:
				print("Circuit Ground Pin:", gndpin);
				gndpin=gndpin.replace(':G','');
				
		#===========================================================================
		#Transistor Lines
		elif ("pch" in newline.lower()) or ("nch" in newline.lower()):
			print("\n=========================")
			name = newline.split()[0];
			print("Name:",name);
			source = newline.split()[1];
			print("Source:",source);
			gate = newline.split()[2];
			print("Gate:",gate);
			drain = newline.split()[3];
			print("Drain:",drain);
			bulk = newline.split()[4];
			print("Bulk:",bulk);
			ttype = newline.split()[5];
			print("Type:",ttype);
			wsize = re.findall('[Ww]=[0-9Ee]*.[0-9Ee]*[\-+0-9]*', newline);
			if is_empty(wsize):
				print("pattern not found W size")
			else:
				wsize = wsize[0].replace('w=','');
				wsize = wsize.replace('W=','');
				wsize = float(wsize);
				print("W Size:",wsize);

			lsize = re.findall('[Ll]=[0-9Ee]*.[0-9Ee]*[\-+0-9]*', newline);
			if is_empty(lsize):
				print("pattern not found L Size")
			else:
				lsize = lsize[0].replace('l=','')
				lsize = lsize.replace('L=','')
				lsize = float(lsize);
				print("L Size:",lsize);

			fingers = re.findall('nf=[0-9]*', newline.lower());
			if is_empty(fingers):
				print("pattern not found: Number of Fingers")
				fingers=1;
			else:
				fingers = fingers[0].replace('nf=','')
				fingers = fingers.replace('NF=','')
				fingers = int(fingers);
				print("Fingers:",fingers);

			if (ttype.lower()=="pch"):
				mos = Transistor(name,source,gate,drain,bulk,ttype,wsize,fingers,lsize);
				ptransistors.append(mos);
			elif (ttype.lower()=="nch"):
				mos = Transistor(name,source,gate,drain,bulk,ttype,wsize,fingers,lsize);
				ntransistors.append(mos);
	f.close();
	#===========================================================================
	#Prints Number of Fetched Transistors
	#===========================================================================
	print("\n\n============================================================");
	print("The Circuit Contains:");
	print("PMOS TRANSISTORS", len(ptransistors));
	print("NMOS TRANSISTORS", len(ntransistors));
	print("\n\n============================================================");
	#===========================================================================
	#Creates Networkx Node Graph and Include Nodes
	#===========================================================================
	G=nx.Graph(); #Creates an graph called G
	color_map=[]; #list that will define node colors
	node_size=[]; #list that will define node sizes
	#-----------------------------------------
	#Searches Nodes and Color them
	#-----------------------------------------
	G.add_node(vddpin); #create vdd node
	color_map.append('green');
	node_size.append(2000);
	G.add_node(gndpin); #create gnd node
	color_map.append('green');
	node_size.append(2000);

	for outpin in outputs:
		G.add_node(outpin);
		color_map.append('magenta');
		node_size.append(1000)
	for n in ptransistors:
		G.add_node(n.get_name());
		color_map.append('red');
		node_size.append(500);
	for n in ntransistors:
		G.add_node(n.get_name());
		color_map.append('blue');
		node_size.append(500);
	for n in ptransistors:
		G.add_edge(n.get_name(),n.get_source());
		color_map.append('yellow');
		node_size.append(100);
		G.add_edge(n.get_name(),n.get_drain());
		color_map.append('yellow');
		node_size.append(100);
	for n in ntransistors:
		G.add_edge(n.get_name(),n.get_source());
		color_map.append('yellow');
		node_size.append(100);
		G.add_edge(n.get_name(),n.get_drain());
		color_map.append('yellow');
		node_size.append(100);

	#===========================================================================
	#Fetches Common Nodes
	#===========================================================================
	common_nodes=[];
	for n in ntransistors:
		for p in ptransistors:
			if (n.get_drain()==p.get_drain()):
				common_nodes.append(n.get_drain());
			elif (n.get_drain()==p.get_source()):
				common_nodes.append(n.get_drain());
			elif (n.get_source()==p.get_drain()):
				common_nodes.append(n.get_source());
			elif (n.get_source()==p.get_source()):
				common_nodes.append(n.get_source());

	common_nodes = list(dict.fromkeys(common_nodes));

	#===========================================================================
	#Searches Euler Paths from COMMON_NODE to VDD
	#===========================================================================
	for common_node in common_nodes:
		print("PATH FROM",common_node ,"TO",vddpin);
		print("============================================================");
		for path in nx.all_simple_paths(G, source=common_node, target=vddpin):
			nodes_path_p=[];
			stack=0;
			if not(gndpin) in path: 
				print("Full Path:", path);
				for node in ptransistors:
					if node.get_name() in path:
						stack=stack+1;
						nodes_path_p.append(node);
				for node in nodes_path_p:
					if node.get_stack()<stack: 
						node.set_stack(stack);
				print("Stack Size =", stack);
			print("============================================================");

	#===========================================================================
	#Searches Euler Paths from COMMON_NODE to VSS
	#===========================================================================
	for common_node in common_nodes:
		print("PATH FROM",common_node ,"TO",gndpin);
		print("============================================================");
		for path in nx.all_simple_paths(G, source=common_node, target=gndpin):
			nodes_path_n=[];
			stack=0;
			if not(vddpin) in path: 
				print("Full Path:", path);
				for node in ntransistors:
					if node.get_name() in path:
						stack=stack+1;
						nodes_path_n.append(node);
				for node in nodes_path_n:
					if node.get_stack()<stack: 
						node.set_stack(stack);
				print("Stack Size =", stack);
			print("============================================================");

	#===========================================================================
	#Drawn Plot
	#===========================================================================
	print("============================================================");
	nx.draw(G,node_size=node_size,node_color = color_map,with_labels=True);
	#===========================================================================
	#Print Calculed Stack Size for Each Transistor
	#===========================================================================
	for node in ptransistors:
		sizew=node.get_wsize()*node.get_stack()*float(wpwn_ratio);
		print("Node:",node.get_name(),"StackFactor:",node.get_stack(),"Calculated Size:", sizew," Original Size:", node.get_wsize());
	for node in ntransistors:
		sizew=node.get_wsize()*node.get_stack();
		print("Node:",node.get_name(),"StackFactor:",node.get_stack(),"Calculated Size:", sizew," Original Size:", node.get_wsize());
	plt.show();

	#===========================================================================
	#Write File
	#===========================================================================
	file = sys.argv[2];
	in_file =open(file,"r");
	file2 = "out_"+file;
	out_file = open(file2,"w");
	for line in in_file:
		found=0;
		for node in ptransistors:
			if node.get_name() in line:
				sizew=node.get_wsize()*node.get_stack()*float(wpwn_ratio);
				out_file.write(node.get_name()+" "+node.get_source() +" " + node.get_gate() +" " + node.get_drain() + " " + node.get_bulk() + " " + node.get_ttype() + " W=" + str(sizew) + " NF="+str(node.get_fingers()) + " L="+str(node.get_lsize())+"\n");
				found=1;
		for node in ntransistors:
			if node.get_name() in line:
				sizew=node.get_wsize()*node.get_stack();
				out_file.write(node.get_name()+" "+node.get_source() +" " + node.get_gate() +" " + node.get_drain() + " " + node.get_bulk() + " " + node.get_ttype() + " W=" + str(sizew) + " NF="+str(node.get_fingers()) + " L="+str(node.get_lsize())+"\n");
				found=1;
		if found !=1:
			out_file.write(line);
	in_file.close();
	out_file.close();
	return 0;

if __name__ == "__main__":
    main();
