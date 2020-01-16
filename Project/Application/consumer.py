import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.consumer import AsyncConsumer
import json
from . models import MachineConfiguration, CreateTaskProfile
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
import random


def get_current_user(session_key):
	session = Session.objects.get(session_key=session_key)
	session_data = session.get_decoded()
	uid = session_data.get('_auth_user_id')
	user = User.objects.get(id=uid)
	return user



class CpuRamConsumer(AsyncJsonWebsocketConsumer):
	async def connect(self):
		await self.accept()
		print('-------',self.scope['session']['team'])
		while 1:
			data = await self.get_live_machine_conf(self.scope['session']['team'])
			live_data = {'data':data, 'total_machines':len(data)}
			await asyncio.sleep(0.5)
			await self.send_json(live_data)
			await asyncio.sleep(0.5)
			await self.send_json(live_data)

	@database_sync_to_async
	def get_live_machine_conf(self, team):
		teamwise_machine_object = MachineConfiguration.objects.filter(team=team)
		# teamwise_machine_object = [(i.id, i.team, i.machine_ip, i.adminuser, i.password, i.cpu_usage, i.ram_usage) for i in teamwise_machine_object]
		teamwise_machine_object = [(i.id, i.team, i.machine_ip, i.adminuser, "*****", random.randrange(1,100), random.randrange(1,100)) for i in teamwise_machine_object]
		return teamwise_machine_object


class ChatConsumer(AsyncConsumer):

	async def websocket_connect(self, event):
		await self.send({
			"type":"websocket.accept"
		})

		await asyncio.sleep(2)

		await self.send({
			"type":"websocket.send",
			"text":"Hello World !"
		})

		

	async def websocket_receive(self, event):
		print('------------received---------',json.loads(event['text']))



class AddMachineConsumer(AsyncConsumer):

	async def websocket_connect(self, event):
		await self.send({
			"type":"websocket.accept"
		})

	async def websocket_receive(self, event):
		
		try:
			machinedetails = json.loads(event['text'])
			try:
				check_exist = await self.check_machine(machinedetails)
			except:
				check_exist = None

			if check_exist == None:
				await self.save_machine(machinedetails)
				response = "Machine Saved Successfully"
			else:
				response = f"Machine allredy present in team : {check_exist.team}"

			await self.send({
				"type":"websocket.send",
				"text": response
			})

		except Exception as e:
			await self.send({
				"type":"websocket.send",
				"text":f"Error while adding machine : {str(e)}"
			})
			
	
	@database_sync_to_async
	def save_machine(self, machinedetails):
		machine_object = MachineConfiguration(team = machinedetails['team'], machine_ip = machinedetails['machineip'],
			adminuser = machinedetails['machineuser'], password = machinedetails['machinepassword'])
		machine_object.save()
		return True

	@database_sync_to_async
	def check_machine(self, machinedetails):
		machine_object = MachineConfiguration.objects.get(machine_ip=machinedetails['machineip'])
		return machine_object


class DisplayAllMachineConsumer(AsyncConsumer):

	async def websocket_connect(self, event):
		await self.send({
			"type":"websocket.accept"
		})

	async def websocket_receive(self, event):
		team = json.loads(event['text'])['team']
		try:
			teamwise_machine_object = await self.show_teamwise_machine(team)
		except Exception as e:
			teamwise_machine_object = str(e)

		await self.send({
				"type":"websocket.send",
				"text": json.dumps(teamwise_machine_object)
		})

	
	@database_sync_to_async
	def show_teamwise_machine(self, team):
		teamwise_machine_object = MachineConfiguration.objects.filter(team=team)
		teamwise_machine_object = [(i.id, i.team, i.machine_ip, i.adminuser, i.password, i.cpu_usage, i.ram_usage) for i in teamwise_machine_object]
		return teamwise_machine_object


class CreateTaskProfileConsumer(AsyncConsumer):

	async def websocket_connect(self, event):
		await self.send({
			"type":"websocket.accept"
		})


		usertaskprofiles = await self.user_task_profile()

		print('----------',usertaskprofiles)

		await self.send({
				"type":"websocket.send",
				"text": json.dumps({'usertaskprofiles':usertaskprofiles})
		})

		

	async def websocket_receive(self, event):
		profiledata = json.loads(event['text'])
		profiledata = {data['name']:data['value'] for data in profiledata}
		print('---------profiledata--------',profiledata,len(profiledata))
		try:
			taskprofile = await self.save_task_profile(profiledata)
			response = 'Profile Saved Successfully'
		except Exception as e:
			response = f"Error while adding taskprofile:{str(e)}"
			
		usertaskprofiles = await self.user_task_profile()

		await self.send({
				"type":"websocket.send",
				"text": json.dumps({'usertaskprofiles':usertaskprofiles,'response':response,})
		})

	@database_sync_to_async
	def save_task_profile(self, profiledata):
		profile_count = CreateTaskProfile.objects.filter(user=self.scope['user']).count()
		print('--------profile_count--------',profile_count)
		if profile_count >= 10 :
			print('------in if-------',profile_count)
			CreateTaskProfile.objects.filter(user=self.scope['user'])[9].delete()
			profile_count = profile_count - 1
		
		CreateTaskProfile.objects.create(user=self.scope['user'],title=f"Task_Profile_{profile_count+1}",select_action=profiledata['select_action'],	
		process_inbox=profiledata['process_inbox'],process_spam=profiledata['process_spam'],compose_mail=profiledata['compose_mail'],\
		archive_or_delete=profiledata['archive_or_delete'],bulk_notspam=profiledata['bulk_notspam'],add_safe_sender=profiledata['add_safe_sender'],\
		color_category=profiledata['color_category'],mark_flag=profiledata['mark_flag'],click_link=profiledata['click_link'],forward_mail=profiledata['forward_mail'],
		report_notspam=profiledata['report_notspam'],inbox_process_count=profiledata['inbox_process_count'],notspam_count=profiledata['notspam_count'],
		delete_count=profiledata['delete_count'],flag_count=profiledata['flag_count'],forward_count=profiledata['forward_count'],
		cc_count=profiledata['cc_count'],ss_count=profiledata['ss_count'],contact_count=profiledata['contact_count'],subject=profiledata['subject'],
		from_name=profiledata['from_name'])

		return True


	@database_sync_to_async
	def user_task_profile(self):
		usertaskprofiles = CreateTaskProfile.objects.filter(user=self.scope['user'])
		usertaskprofiles = [(i.id, i.title) for i in usertaskprofiles]
		return usertaskprofiles
