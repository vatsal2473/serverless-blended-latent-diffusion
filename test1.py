import banana_dev as banana

model_inputs = {'prompt': 'realistic field of grass', 
                'input_image': 'https://tmpfiles.org/dl/474606/img.png', 
                'mask_image': 'https://tmpfiles.org/dl/474608/mask.png'}

out = banana.run('173af88f-2811-4b69-b888-8cc0047abfa1', '80bb1971-3eb2-452d-84e0-4b00de2e03f7', model_inputs)
print(out)