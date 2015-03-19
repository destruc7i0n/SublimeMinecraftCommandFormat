import sublime
import sublime_plugin

class MinecraftFormatBaseCommand(sublime_plugin.TextCommand):
	"""This code is almost entirely by @Texelelf, all credit goes to him."""
	def indent(ct):
		return "".join(["\t" for i in xrange(ct)])

	def strexplode(command):
		coms = []
		if not command:
			return coms
		i = 0
		line = ""
		inquote = 0
		for c in xrange(len(command)):
			if command[c] == "{":
				if inquote:
					line += command[c]
				else:
					if line:
						coms.append(indent(i)+line+"\n")
						line = ""
					coms.append(indent(i)+"{\n")
					i += 1
			elif command[c] == "}":
				if inquote:
					line += command[c]
				else:
					if line:
						coms.append(indent(i)+line+"\n")
						line = ""
					i -= 1
					line += command[c]
			elif command[c] == "[":
				if inquote:
					line += command[c]
				else:
					if line:
						coms.append(indent(i)+line+"\n")
						line = ""
					coms.append(indent(i)+"[\n")
					i += 1
			elif command[c] == "]":
				if inquote:
					line += command[c]
				else:
					if line:
						coms.append(indent(i)+line+"\n")
						line = ""
					i -= 1
					line += command[c]
			elif command[c] == '\"':
				if command[c-1] != "\\":
					inquote ^= 1
				line += command[c]
			elif command[c] == ",":
				if inquote:
					line += command[c]
				else:
					coms.append(indent(i)+line+",\n")
					line = ""
			else:
				line += command[c]
		else:
			if line:
				coms.append(indent(i)+line+"\n")
		return coms

class MinecraftFormatCommand(MinecraftFormatBaseCommand):
	""" Pretty Print a Minecraft Command """
	def run(self, edit):
		for region in self.view.sel():

			# If no selection, use the entire file as the selection
			if region.empty():
				selection = sublime.Region(0, self.view.size())
			else:
				selection = region

			if "{" in selection:
				mdatapos = selection.find("{")
				outputlines.append(selection[:mdatapos]+"\n")
				outputlines+=strexplode(selection[mdatapos:])
			else:
				outputlines.append(str(selection)+"\n")			
#			obj = self.strexplode(self.view.substr(selection))
			self.view.replace(edit, selection, ("".join(outputlines)))
